from router import db,bcrypt
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__='Users'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)

    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=bcrypt.generate_password_hash(password)
    
    def __repr__(self):
        return '{}-{}-{}'.format(self.username,self.email,self.password)

class Profile(db.Model):
    __tablename__='Profile'

    id=db.Column(db.Integer,primary_key=True)
    fullname=db.Column(db.String,nullable=False)
    address1=db.Column(db.String,nullable=False)
    address2=db.Column(db.String,nullable=False)
    city=db.Column(db.String,nullable=False)
    state=db.Column(db.String,nullable=False)
    zipcode=db.Column(db.String,nullable=False)
    profile_username=db.Column(db.String,nullable=False)

    def __init__(self,fullname,address1,address2,city,state,zipcode,profile_username):
        self.fullname=fullname
        self.address1=address1
        self.address2=address2
        self.city=city
        self.state=state
        self.zipcode=zipcode
        self.profile_username=profile_username

    def __repr__(self):
        return '{}-{}-{}-{}-{}-{}-{}'.format(self.fullname,self.address1,self.address2,self.city,self.state,self.zipcode,self.profile_username)

class Quote(db.Model):
    __tablename__='Quote'

    id=db.Column(db.Integer,primary_key=True)
    quote_username=db.Column(db.String,nullable=False)
    gallons_amount=db.Column(db.Integer,nullable=False)
    delivery_address=db.Column(db.String,nullable=False)
    delivery_date=db.Column(db.String,nullable=False)
    price_per_gallon=db.Column(db.Integer,nullable=False)
    total_price=db.Column(db.Integer,nullable=False)

    def __init__(self,quote_username,gallons_amount,delivery_address,delivery_date,price_per_gallon,total_price):
        self.quote_username=quote_username
        self.gallons_amount=gallons_amount
        self.delivery_address=delivery_address
        self.delivery_date=delivery_date
        self.price_per_gallon=price_per_gallon
        self.total_price=total_price

    def __repr__(self):
        return '{}-{}-{}-{}-{}-{}'.format(self.quote_username,self.gallons_amount,self.delivery_address,self.delivery_date,self.price_per_gallon,self.total_price)

class CalculatedPrices(db.Model):
    __tablename__='Calculated Prices'

    id=db.Column(db.Integer,primary_key=True)
    calculated_price_username=db.Column(db.String,nullable=False)
    price_per_gallon=db.Column(db.Integer,nullable=False)
    total_price=db.Column(db.Integer,nullable=False)

    def __init__(self,calculated_price_username,price_per_gallon,total_price):
        self.calculated_price_username=calculated_price_username
        self.price_per_gallon=price_per_gallon
        self.total_price=total_price
    
    def __repr__(self):
        return '{}-{}'.format(self.price_per_gallon,self.total_price)