from flask import redirect, render_template, url_for, flash, request, session, current_app
#from flask_session import Session
from shop import db, app, photos
from .models import Category, Addproduct
from .forms import Addproducts
import secrets, os


def categories():
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/')
def home():
    products = Addproduct.query.filter(Addproduct.stock > 0)
    return render_template('products/index.html', products = products, categories=categories())

@app.route('/ourmenu')
def menu():
    return render_template('products/ourmenu.html')

@app.route('/category/<int:id>')
def get_category(id):
    category = Addproduct.query.filter_by(category_id=id)
    return render_template('products/index.html', category = category, categories = categories())



@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    if request.method=="POST":
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html')

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatecategory.html', title='Update Category Page', updatecat=updatecat)


@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The category {category.name} can not be deleted', 'warning')
    return redirect(url_for('admin'))




@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        desc = form.description.data
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'))

        addpro = Addproduct(name=name,price=price,discount=discount,stock=stock,desc=desc,category_id=category, image_1=image_1)
        db.session.add(addpro)
        flash(f'The product {name} has been added to database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add Product', categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))

    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.category_id = category
        product.desc = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'))
            except:
                product.image_1 = photos.save(request.files.get('image_1'))

        db.session.commit()
        flash(f'The product has been updated', 'success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.description.data=product.desc

    return render_template('products/updateproduct.html', form=form, categories=categories, product=product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):

    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images" + product.image_1))
        
        except Exception as e:
            print(e)
        #try:
        #    os.unlink(os.path.join(current_app.root_path, "static/images" + product.image_1))
        
        #except Exception as e:
        #    print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    
    flash(f'Cannot delete the product', 'danger')
    return redirect(url_for('admin'))

