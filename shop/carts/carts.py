from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from shop.products.models import Addproduct
from shop.products.routes import categories
from decimal import Decimal


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False




@app.route('/Addcart', methods=['POST'])
def AddCart():
    try:
        product_id=request.form.get('product_id')
        quantity = int(request.form.get ('quantity'))
        product = Addproduct.query.filter_by(id=product_id).first()
        
        if request.method == "POST":
            DictItems = {product_id:{'name':product.name, 'price':float(product.price), 'quantity':quantity}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item ['quantity'] += 1

                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    for key, product in session['Shoppingcart'].items():
        subtotal += float(product['price']) * int(product['quantity'])
        
    return render_template('products/carts.html', subtotal=subtotal, categories=categories())

@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('home'))
    except Exception as e:
        print(e)


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))

    if request.method =="POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key , item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('The item has been updated')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))







