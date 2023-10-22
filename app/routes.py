from datetime import datetime
import uuid
from app import app, db, load_user
from app.models import Challenge, User, UserChallenge, Course
from app.forms import SignUpForm, SignInForm
from flask import flash, jsonify, render_template, redirect, session, url_for, request
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
    favorited_challenges = current_user.favorites  # Fetching the favorite challenges

    return render_template('user_profile.html', user=current_user, userchallenge = userChallenges, favorited_challenges=favorited_challenges)

@app.route('/courses', defaults={'courseid': None}, methods=['GET', 'POST'])
@app.route('/courses/<courseid>', methods=['GET', 'POST'])
@login_required
def courses(courseid):
    if courseid:

        challenges = Challenge.query.filter_by(courseid=courseid).all()
        return render_template('challengelist.html', challenges=challenges)
    
    # newChallenge = Challenge(challengeid='ooga booga', courseid='1050', description='put ooga in booga', difficulty='easy')
    # newChallenge1 = Challenge(challengeid='oogity boogity', courseid='CS1050', description='Make an array of 10 boogities', difficulty='medium')
    # newChallenge2 = Challenge(challengeid='unga bunga', courseid='CS1050', description='make unga a bunga', difficulty='hard')
    # newChallenge3 = Challenge(challengeid='ooga super', courseid='CS1051', description='make an ooga array', difficulty='easy')
    # newChallenge4 = Challenge(challengeid='Web ooga', courseid='CS1051', description='make ooga website', difficulty='medium')
    # newChallenge5 = Challenge(challengeid='Web booga', courseid='CS1051', description='make booga website', difficulty='hard')
    # newChallenge6 = Challenge(challengeid='aurrhe', courseid='CS1052', description='arf array', difficulty='easy')

    # db.session.add(newChallenge)
    # db.session.add(newChallenge1)
    # db.session.add(newChallenge2)
    # db.session.add(newChallenge3)
    # db.session.add(newChallenge4)
    # db.session.add(newChallenge5)
    # db.session.add(newChallenge6)

    # newCourse = Course(courseid='CS1050', description='Computer Science 1')
    # newCourse1 = Course(courseid='CS1051', description='Computer Science 2')
    # newCourse2 = Course(courseid='CS1052', description='Computer Science 3')

    # db.session.add(newCourse)
    # db.session.add(newCourse1)
    # db.session.add(newCourse2)
    # db.session.commit()
    # If no specific courseid is provided, list all courses


    courses = Course.query.all()
    return render_template('courselist.html', courses=courses)

@app.route('/completed', methods=['GET', 'POST'])
@login_required
def completed():
    userchallenge = UserChallenge.query.filter_by(user_id=current_user.id).all()
    # fakeUserChallenge = UserChallenge(challengeid='unga bunga', user_id='Hi')
    # db.session.add(fakeUserChallenge)
    # db.session.commit()

    return render_template('completed.html', user=current_user, userChallenge=userchallenge)

@app.route('/favorite_challenge/<challenge_id>', methods=['POST'])
@login_required
def add_favorite_challenge(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if challenge not in current_user.favorites:
        current_user.favorites.append(challenge)
        db.session.commit()
    return '', 204

@app.route('/favorite_challenge/<challenge_id>', methods=['DELETE'])
@login_required
def remove_favorite_challenge(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if challenge in current_user.favorites:
        current_user.favorites.remove(challenge)
        db.session.commit()
    return '', 204



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
