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

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<UserPreference {self.category} for User {self.user_id}>'
    

class RatingReview(db.Model):
    __tablename__ = 'rating_review'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(80), db.ForeignKey('item.Item_ID'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<RatingReview(id='{self.id}', item_id='{self.item_id}', rating='{self.rating}', review='{self.review}')>"
