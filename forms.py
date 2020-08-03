from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField,DecimalField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp, Optional

class LoginForm(FlaskForm):
    username = TextField('Enter Username: ',validators=[DataRequired()])
    password = PasswordField('Enter Password: ',validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = TextField('Enter a Username: ',validators=[DataRequired(),Length(min=5,max=30)])
    email = TextField('Enter an Email: ',validators=[DataRequired(),Email(message=None),Length(min=7,max=50)])
    password = PasswordField('Enter a Password: ',validators=[DataRequired(),Length(min=8,max=30)])
    confirm_password = PasswordField('Confirm Password: ',validators=[DataRequired(),Length(min=8,max=30),EqualTo('password',message='Passwords must match!')])

class ProfileForm(FlaskForm):
    fullname=TextField('Enter Fullname: ',validators=[DataRequired(),Length(min=2,max=50)])
    address1=TextField('Enter Address 1: ',validators=[DataRequired(),Length(max=100)])
    address2=TextField('Enter Address 2: ',validators=[Length(max=100)])
    city=TextField('Enter City: ',validators=[DataRequired(),Length(max=100)])
    state_abbreviations= [('AL','AL'),('AK','AK'),('AZ','AZ'),('AR','AR'),('CA','CA'), ('CO','CO'),('CT','CT'), ('DE','DE'), ('FL','FL'), ('GA','GA'), ('HI','HI'), ('ID','ID'), ('IL','IL'), ('IN','IN'), ('IO','IO'), ('KS','KS'),('KY','KY'),('LA','LA'), ('ME','ME'), ('MD','MD'),('MA','MA'), ('MI','MI'), ('MN','MN'), ('MS','MS'), ('MO','MO'), ('MT','MT'), ('NE','NE'), ('NV','NV'),('NH','NH') , ('NJ','NJ'), ('NM','NM'), ('NV','NV'), ('NC','NC'), ('ND','ND'), ('OH','OH'), ('OK','OK'), ('OR','OR'), ('PA','PA'), ('RI','RI'), ('SC','SC'), ('SD','SD'), ('TN','TN'), ('TX','TX'), ('UT','UT'), ('VT','VT'), ('VA','VA'), ('WA','WA'), ('WV','WV'), ('WI','WI'), ('WY','WY')]
    state=SelectField(validators=[DataRequired()],choices=state_abbreviations,coerce=str)
    zipcode=TextField('Enter Zipcode: ',validators=[DataRequired(),Length(min=5, max=9),Regexp(regex='[0-9]')])

class QuoteForm(FlaskForm):
    gallons=IntegerField('Enter Gallons Amount: ',validators=[DataRequired()])
    delivery_date= DateField('Delivary Date: ',format='%Y-%m-%d',validators=[DataRequired()])
    delivery_address=TextField('Enter Delivery Address: ',validators=[Optional()])
    suggested_price_per_gallons = IntegerField('Price per Gallon: ', render_kw={'readonly': True},validators=[Optional()])
    total_price=IntegerField('Total Price: ',validators=[Optional()])