from app import db

class Items(db.Model):
    __tablename__ = 'item'
    Item_ID = db.Column(db.String(80),unique=True, primary_key=True)
    sku = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    item_desc = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    item_star = db.Column(db.Integer, nullable=False)
    itme_sizes = db.Column(db.String(120),  nullable=True)
    color = db.Column(db.String(120), nullable=False)
    pic = db.Column(db.Text) 
    def __repr__(self):
        return f"<Products(Item_ID='{self.Item_ID}', name='{self.name}',price ='{self.price},category ='{self.category})>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

