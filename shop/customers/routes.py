from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos, bcrypt, login_manager
from flask_login import login_required, current_user, logout_user, login_user
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register, CustomerOrder
import secrets
import os
import stripe


#app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51IgEu2GZcd7iMlawQNB029EogD17zVRAPc2F6Jt1yLp25bDdsYQtNZMiqISBSYG9UN1fPPgXGHcJVopzeN8yaRvx00a2P3qce8'
#app.config['STRIPE_SECRET_KEY'] = 'sk_test_51IgEu2GZcd7iMlaw10dT4ffRfhRqPzY60w3CcLVVHmbHhLQf7Svaio9Kh05QgkoUm0ybF0hjeKecBJ80BlWDUAyP00HvhejDV5'

publishable_key = 'pk_test_51IgEu2GZcd7iMlawQNB029EogD17zVRAPc2F6Jt1yLp25bDdsYQtNZMiqISBSYG9UN1fPPgXGHcJVopzeN8yaRvx00a2P3qce8'

stripe.api_key = 'sk_test_51IgEu2GZcd7iMlaw10dT4ffRfhRqPzY60w3CcLVVHmbHhLQf7Svaio9Kh05QgkoUm0ybF0hjeKecBJ80BlWDUAyP00HvhejDV5'

@app.route('/payment', methods=['POST'])
@login_required
def payment():
    amount = request.form.get('amount')
    invoice = request.form.get('invoice')

    charge = stripe.Charge.create(
        amount=amount,
        currency='eur',
        source = request.form['stripeToken']
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    flash('Your order has been placed', 'success')
    return redirect(url_for('thanks'))


@app.route('/customer/thank')
def thanks():
    return render_template('customer/thank.html')


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, telephone=form.telephone.data, address=form.address.data, eircode=form.eircode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data}, thank you registering', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are logged in now', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password', 'danger')
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            return redirect(url_for('orders', invoice=invoice))

        except Exception as e:
            print(e)
            flash('Something went wrong while processing your order', 'success')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        subTotal = 0
        grandTotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            subTotal += float(product['price']) * int(product['quantity'])
            grandTotal = (f"{subTotal}")
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, subTotal=subTotal, grandTotal=grandTotal, customer=customer, orders=orders)
