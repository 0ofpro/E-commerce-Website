from app import app, db
from flask import render_template, request, redirect, url_for,flash,session
from app.models import Items
from sqlalchemy.sql import text,or_
from math import ceil


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/show_products', methods=['GET'])
def show_products():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Query database to get movies for the current page
    products = Items.query.paginate(page=page, per_page=per_page)

    # Calculate total number of pages
    total_pages = ceil(products.total / per_page)

    return render_template('show_products.html', products=products, page=page, total_pages=total_pages)

@app.route('/products')
def products():
    return render_template('products.html')