from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Product, User, Order
from app import db
import cloudinary.uploader
import os

main = Blueprint('main', __name__)

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'coachfactory2026'

# ─── PUBLIC ROUTES ───────────────────────────────────────

@main.route('/')
def index():
    featured = Product.query.limit(3).all()
    return render_template('index.html', featured=featured)

@main.route('/products')
def products():
    category = request.args.get('category', 'All')
    if category == 'All':
        all_products = Product.query.all()
    else:
        all_products = Product.query.filter_by(category=category).all()
    categories = ['All', 'Shoulder Bags', 'Totes', 'Crossbody', 'Mini Bags']
    return render_template('products.html', products=all_products,
                           categories=categories, active=category)

@main.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related = Product.query.filter_by(category=product.category)\
                     .filter(Product.id != product_id).limit(3).all()
    return render_template('product_detail.html', product=product, related=related)

@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash('Please login to add items to your bag.', 'warning')
        return redirect(url_for('main.login'))
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    flash('Item added to your bag!', 'success')
    return redirect(url_for('main.cart'))

@main.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    cart_items = Product.query.filter(Product.id.in_(cart_ids)).all()
    total = sum(item.price for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@main.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    session['cart'] = cart
    return redirect(url_for('main.cart'))

# ─── AUTH ROUTES ─────────────────────────────────────────

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('main.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists.', 'danger')
            return redirect(url_for('main.register'))

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Welcome to Coach Factory, {first_name}!', 'success')
        return redirect(url_for('main.account'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.first_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.account'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main.route('/account')
@login_required
def account():
    return render_template('account.html')

# ─── ADMIN ROUTES ────────────────────────────────────────

@main.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    products = Product.query.all()
    users = User.query.all()
    return render_template('admin_dashboard.html', products=products, users=users)

@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Welcome back, Admin!', 'success')
            return redirect(url_for('main.admin'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin_login.html')

@main.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.admin_login'))

@main.route('/admin/add_product', methods=['GET', 'POST'])
def admin_add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        description = request.form.get('description')
        category = request.form.get('category')
        image_urls = []

        files = request.files.getlist('images')
        for file in files:
            if file and file.filename != '':
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder='coach_factory',
                    transformation=[
                        {'width': 800, 'height': 1000,
                         'crop': 'fill', 'gravity': 'auto'}
                    ]
                )
                image_urls.append(upload_result.get('secure_url', ''))

        product = Product(
            name=name,
            price=price,
            description=description,
            category=category,
            images=','.join(image_urls)
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('main.admin'))
    return render_template('admin_add_product.html')

@main.route('/admin/delete_product/<int:product_id>')
def admin_delete_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('main.admin'))

@main.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.description = request.form.get('description')
        product.category = request.form.get('category')

        files = request.files.getlist('images')
        new_urls = []
        for file in files:
            if file and file.filename != '':
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder='coach_factory',
                    transformation=[
                        {'width': 800, 'height': 1000,
                         'crop': 'fill', 'gravity': 'auto'}
                    ]
                )
                new_urls.append(upload_result.get('secure_url', ''))

        if new_urls:
            existing = product.get_images()
            all_images = existing + new_urls
            product.images = ','.join(all_images)

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.admin'))
    return render_template('admin_add_product.html', product=product)