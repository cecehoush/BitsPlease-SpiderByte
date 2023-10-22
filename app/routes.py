from datetime import datetime
import uuid
from app import Submission, app, db, load_user
from app.models import User
from app.forms import SignUpForm, SignInForm
from app.codetest import TestUserCode
from app.runcode import executePython
from flask import flash, render_template, redirect, session, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt


@app.route('/')
@app.route('/authentication')
@app.route('/authentication.html')
def authentication(): 
    return render_template('authentication.html')

@app.route('/submit', methods=['POST'])
def submit_code():
    code = request.form.get('code')
    if code:
        submission = Submission(code=code)
        print(code)
        db.session.add(submission)
        db.session.commit()
        return "Code submitted successfully!"
    return "Error in submission!", 400

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
            return redirect('/userProfile')
        else:
            return ('<p>Incorrect Password</p>')
    return render_template('signin.html', form=signInForm)


@app.route('/editor', methods=['GET', 'POST'])
def code_editor():
    if request.method == 'POST':
        user_code = request.form['code']
        print(TestUserCode.test_add(user_code))
        result = executePython(user_code)
        return result  # This sends the result back as plain text to the frontend
    return render_template('codeEditor.html')

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
