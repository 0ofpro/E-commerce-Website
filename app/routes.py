from app import app, db
from flask import render_template, request, redirect, url_for,flash,session
from sqlalchemy.sql import text
from math import ceil


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/product')
def products():
    return render_template('product.html')