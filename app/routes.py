from app import app, db
from flask import render_template, request, redirect, url_for,flash,session,send_from_directory,abort
from app.models import Items,User,UserPreference
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

    
@app.route('/product/<string:Item_ID>')
def product_page(Item_ID):
    # Retrieve the product details from the database based on the product ID
    product = Items.query.filter_by(Item_ID=Item_ID).first()
    if product is None:
        abort(404)
    product1 = Items.query.filter_by(Item_ID=Item_ID).first()
    image_path = product1.pic
    return render_template('product.html', product=product,image_path=image_path)

@app.route('/product/<string:Item_ID>/rating_review', methods=['GET', 'POST'])
def product_rating_review(Item_ID):
    if request.method == 'POST':
        rating = request.form.get('rating')
        review = request.form.get('review')
        # Process rating and review data, e.g., save to database

        return 'Rating: {}, Review: {}'.format(rating, review)
    return render_template('rating_review.html', Item_ID=Item_ID)


@app.route('/search', methods=['GET'])
def search_products():
    # Get the search query from the request
    query = request.args.get('query', '')

    # Get filter options from the request
    price = request.args.get('price')
    category = request.args.get('category')
    item_star = request.args.get('item_star')

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query for products
    query_base = Items.query

    # Apply filters if provided
    if price:
        query_base = query_base.filter(Items.price <= int(price))
    if category:
        query_base = query_base.filter(Items.category.ilike(f'%{category}%'))
    if item_star:
        query_base = query_base.filter(Items.item_star >= int(item_star))

    # Filter products based on search query
    if query:
        # If both query and filters are provided, filter by both
        query_results = query_base.filter(or_(Items.name.ilike(f'%{query}%'), Items.item_desc.ilike(f'%{query}%')))
    else:
        # If only filters are provided, use filtered query
        query_results = query_base

    # Fetch unique categories from the database
    categories = Items.query.with_entities(Items.category).distinct().all()
    categories = [category[0] for category in categories]

    # Paginate the results
    products = query_results.paginate(page=page, per_page=per_page)

    # Calculate total number of pages
    total_pages = products.total // per_page + (products.total % per_page > 0)

    return render_template('show_products.html', products=products, page=page, total_pages=total_pages, categories=categories)

@app.route('/product_pic')
def product_pic():
    product1 = Items.query.filter_by(Item_ID='P10001').first()
    if product1 is None:
        abort(404)
    image_path = product1.pic
    return render_template('product_pic.html', image_path=image_path)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        categories = request.form.getlist('categories[]')

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        for category in categories:
            preference = UserPreference(user_id=new_user.id, category=category)
            db.session.add(preference)
        db.session.commit()

        session['username'] = username
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Authentication successful, store user id in session
            session['username'] = user.username
            return redirect(url_for('dashboard', username=user.username))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Retrieve username from session
    username = session.get('username')
    if username:
        # Fetch user preferences
        user = User.query.filter_by(username=username).first()
        preferences = UserPreference.query.filter_by(user_id=user.id).all()
        
        # Extract categories from user preferences
        categories = [preference.category for preference in preferences]
        
        # Fetch recommended products based on user preferences
        recommended_products = Items.query.filter(Items.category.in_(categories)).order_by(Items.item_star.desc()).limit(5).all()
        
        return render_template('dashboard.html', username=username, recommended_products=recommended_products)
    else:
        return redirect(url_for('login'))