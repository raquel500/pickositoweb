from shop import db
#from datetime import datetime

class Addproduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(18,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    #pub_date = db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
    
    #category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    #category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))


    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Addproduct %r>' % self.name

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)

#class Category(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(30), nullable=True, unique=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)


db.create_all()