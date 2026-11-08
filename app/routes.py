from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.models import Product
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

@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(url_for('main.products'))

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

# ─── ADMIN ROUTES ────────────────────────────────────────

@main.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect(url_for('main.admin_login'))
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

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