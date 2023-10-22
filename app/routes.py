from datetime import datetime
import uuid
from app import app, db, load_user
from app.models import Challenge, User, UserChallenge, Course
from app.forms import SignUpForm, SignInForm
from flask import flash, render_template, redirect, session, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt


@app.route('/')
@app.route('/authentication')
@app.route('/authentication.html')
def authentication(): 
    return render_template('authentication.html')

# sign-in functionality from previous homework
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    signInForm = SignInForm()

    # checkMota = load_user('tmota')
    # if checkMota == None:
    #     newAdmin = Admin(id='tmota', email='admin', password=bcrypt.hashpw('1'.encode('utf-8'), bcrypt.gensalt()), title='Professor', name='Thyago Mota')
    #     db.session.add(newAdmin)
    #     # More products can be added in the /add_product page
    #     db.session.commit()

    if signInForm.validate_on_submit():
        userID = signInForm.id.data
        userPass = signInForm.password.data.encode('utf-8')

        checkUser = load_user(userID)
        if checkUser == None:
            return ('<p>No user found</p>')
        

        if bcrypt.checkpw(userPass, checkUser.password):
            login_user(checkUser)
            print("match")
            return redirect('/users/profile')
        else:
            return ('<p>Incorrect Password</p>')
    return render_template('signin.html', form=signInForm)

# sign-up functionality from previous homework
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    signUp = SignUpForm()

    if signUp.validate_on_submit():
        password = signUp.password.data
        password_confirm = signUp.password_confirm.data

        existing_user = load_user(signUp.id.data)
        if existing_user:
            flash('User already exists, Please choose a different one', 'error')
            return redirect(url_for('users_signup'))

        if password == password_confirm:
            hashedPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            newUser = User(id=signUp.id.data, password=hashedPass)
            db.session.add(newUser)
            db.session.commit()
            return redirect('/authentication')
        else:
            return ('<p>Password didn\'t match confirmation</p>')
        
    return render_template('signup.html', form=signUp)

    
# sign-out functionality from previous homework
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    if users_signout:
        logout_user()
        return redirect('/authentication')
    
@app.route('/users/profile', methods=['GET', 'POST'])
@login_required
def user_profile():

    userChallenges = UserChallenge.query.filter_by(user_id=current_user.id).all()
    return render_template('user_profile.html', user=current_user, userchallenge = userChallenges)

@app.route('/courses', defaults={'courseid': None}, methods=['GET', 'POST'])
@app.route('/courses/<courseid>', methods=['GET', 'POST'])
def courses(courseid):
    if courseid:
        # Fetch challenges for the specific course
        challenges = Challenge.query.filter_by(courseid=courseid).all()
        return render_template('challengelist.html', challenges=challenges)
    
    # If no specific courseid is provided, list all courses
    courses = Course.query.all()
    return render_template('courselist.html', courses=courses)


 # switch to add courses    
# @app.route('/add_product', methods=['GET', 'POST'])
# @login_required 
# def add_product():
#     form = ProductForm()
#     if not isinstance(current_user._get_current_object(), Admin):
#         return redirect(url_for('products'))
#     if form.validate_on_submit():
#         code = form.code.data
#         price = form.price.data
#         windowOrDoor = form.type.data
#         description = form.description.data
#         available = form.available.data

#         new_product = Product(code=code, price=price, type=windowOrDoor, description=description, available=available)
#         db.session.add(new_product)
#         db.session.commit()

#         return redirect(url_for('products'))
    
#     return render_template('add_product.html', form=form)
