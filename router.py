from flask import Flask, render_template, request,redirect,url_for,flash,session
from flask_login import login_required, current_user, LoginManager, login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import LoginForm,RegisterForm,ProfileForm,QuoteForm
from pricing_module import Pricing_Module

app = Flask(__name__)
app.config["SECRET_KEY"] = '\xcd\xb8\x14\xb8;\xee\xbf\x88Ig\xa9\xfd\x99\x86*\xbf\x91t\xa6\x91lZ\xb0\xf6'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data_base.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager()
login_manager.init_app(app)
from models import *
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==int(user_id)).first()

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('profile')
    login_form=LoginForm(request.form)
    if login_form.validate_on_submit():
            logging_user=User.query.filter_by(username=request.form['username']).first()
            if logging_user is not None:
                if bcrypt.check_password_hash(logging_user.password,request.form['password']):
                    login_user(logging_user)
                    profile_exists=Profile.query.filter_by(profile_username=current_user.username).first()
                    if profile_exists is None:
                        flash('Complete Profile to Access Other Pages.')
                        return redirect(url_for('profile'))
                    flash('Successful Login!')
                    session['delivery_address'] = profile_exists.address1 + ', ' + profile_exists.city + ', ' + profile_exists.state + ' ' + profile_exists.zipcode
                    session['state']=profile_exists.state
                    return redirect(url_for('quote'))
                else:
                    flash('Incorrect Password.')
            else:
                flash('User Not found.')
    return render_template('login.html',form=login_form)

@app.route('/register',methods=['GET','POST'])
def register():
    register_form=RegisterForm()
    if register_form.validate_on_submit():
        entered_username=User.query.filter_by(username=register_form.username.data).first()
        entered_email=User.query.filter_by(email=register_form.email.data).first()
        if entered_username is not None:
            flash('Username is already taken. Choose another username.')
            return render_template('register.html',form=register_form)
        if entered_email is not None:
            flash('Email is already used for a different account. Choose another email.')
            return render_template('register.html',form=register_form)
        new_user=User(username=register_form.username.data,email=register_form.email.data,password=register_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Registerd!')
        flash('Please Login.')
        return redirect(url_for('login'))
    return render_template('register.html',form=register_form)

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    profile_form=ProfileForm()
    client_profile=Profile.query.filter_by(profile_username=current_user.username).first()
    if profile_form.validate_on_submit():
        session['delivery_address'] = profile_form.address1.data + ', ' + profile_form.city.data + ', ' + profile_form.state.data + ' ' + profile_form.zipcode.data
        session['state']=profile_form.state.data
        if client_profile is None:
            new_profile=Profile(fullname=profile_form.fullname.data,address1=profile_form.address1.data,address2=profile_form.address2.data,city=profile_form.city.data,state=profile_form.state.data,zipcode=profile_form.zipcode.data,profile_username=current_user.username)
            db.session.add(new_profile)
            db.session.commit()
            flash('Profile Updated!')
            return redirect(url_for('quote'))
        else:
            client_profile.fullname=profile_form.fullname.data
            client_profile.address1=profile_form.address1.data
            client_profile.address2=profile_form.address2.data
            client_profile.city=profile_form.city.data
            client_profile.state=profile_form.state.data
            client_profile.zipcode=profile_form.zipcode.data
            db.session.commit()
    if client_profile is not None:
        profile_form.fullname.data=client_profile.fullname
        profile_form.address1.data=client_profile.address1
        profile_form.address2.data=client_profile.address2
        profile_form.city.data=client_profile.city
        profile_form.state.data=client_profile.state
        profile_form.zipcode.data=client_profile.zipcode
        print(profile_form.state.data)
    return render_template('profile.html',form=profile_form)

@app.route('/history',methods=['GET'])
@login_required
def history():
    profile_exists=Profile.query.filter_by(profile_username=current_user.username).first()
    if profile_exists is None:
        flash('Complete Profile to Continue.')
        return redirect(url_for('profile'))
    past_quotes=Quote.query.filter_by(quote_username=current_user.username)
    return render_template('history.html',past_quotes=past_quotes)

@app.route('/quote',methods=['GET','POST'])
@login_required
def quote():
    profile_exists=Profile.query.filter_by(profile_username=current_user.username).first()
    if profile_exists is None:
        flash('Complete Profile to Continue.')
        return redirect(url_for('profile'))
    quote_form=QuoteForm()
    quote_form.delivery_address.data=session['delivery_address']
    quote_form.suggested_price_per_gallons.data='Enter Gallons Amount to Calculate'
    quote_form.total_price.data='Enter Gallons Amount to Calculate'
    if quote_form.validate_on_submit():
        if request.form['submit'] == 'Get Quote Pricing':
            ordered_before=Quote.query.filter_by(quote_username=current_user.username).first()
            pm_obj=Pricing_Module()
            if ordered_before is not None:
                session['suggested_price'],session['total_amount_due'] = pm_obj.pricing_module(quote_form.gallons.data,session['state'],True)
            else:
                session['suggested_price'],session['total_amount_due'] = pm_obj.pricing_module(quote_form.gallons.data,session['state'],False)
            quote_form.suggested_price_per_gallons.data=session['suggested_price']
            quote_form.total_price.data=session['total_amount_due']
        else:
            submitted_quote=Quote(quote_username=current_user.username,gallons_amount=quote_form.gallons.data,delivery_address=session['delivery_address'],delivery_date=quote_form.delivery_date.data,price_per_gallon=session['suggested_price'],total_price=session['total_amount_due'])
            db.session.add(submitted_quote)
            db.session.commit()
            flash('Quote Order has been successfuly submitted')
            return redirect(url_for('quote'))
    return render_template('quote.html',form=quote_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successful!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)