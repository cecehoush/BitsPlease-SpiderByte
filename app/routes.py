from datetime import datetime
import uuid
from app import Submission, app, db, load_user
from app.codetest import test_user_code
from app.models import Admin, Challenge, User, UserChallenge, Course, TestCase
from app.forms import ChallengeForm, SignUpForm, SignInForm, TestCaseForm
from flask import flash, render_template, redirect, session, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt


@app.route('/')
@app.route('/authentication')
@app.route('/authentication.html')
def authentication(): 
    return render_template('authentication.html')

# @app.route('/submit', methods=['POST'])
# def submit_code():
#     code = request.form.get('code')
#     if code:
#         submission = Submission(code=code)
#         print(code)
#         db.session.add(submission)
#         db.session.commit()
#         return "Code submitted successfully!"
#     return "Error in submission!", 400

# sign-in functionality from previous homework
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    signInForm = SignInForm()

    checkAdmin = load_user('spider')
    if checkAdmin == None:
        newAdmin = Admin(id='spider', password=bcrypt.hashpw('1'.encode('utf-8'), bcrypt.gensalt()))
        db.session.add(newAdmin)

        db.session.commit()

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


@app.route('/challenge/<challengeid>', methods=['GET', 'POST'])
def challenge(challengeid):
    challenge_data = Challenge.query.get(challengeid)
    if not challenge_data:
        return "Challenge not found", 404

    if request.method == 'POST':
        user_code = request.form['code']

        challengeCheck = challenge_data.test_cases
        all_test_cases = [test_case for test_case in challengeCheck] 
        
        results = test_user_code(user_code, all_test_cases) 

        if all(results):  # Check if all test cases passed (ugly)
            previouslyCompleted = UserChallenge.query.filter_by(challengeid=challengeid, user_id=current_user.id).first()
            if not(previouslyCompleted):
                passedChallenge = UserChallenge(challengeid=challengeid, user_id=current_user.id)
                db.session.add(passedChallenge)
                db.session.commit()
            else:
                return "You have already completed this challenge!"
            return "All test cases passed!", 200
        else:
            failed_tests = [i+1 for i, res in enumerate(results) if not res]
            return f"Failed test cases: {', '.join(map(str, failed_tests))}", 400

    return render_template('challengePage.html', challenge=challenge_data)



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
            flash('Password didn\'t match confirmation', 'error')
            return redirect(url_for('users_signup'))
        
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

        is_admin = isinstance(current_user._get_current_object(), Admin)
        challenges = Challenge.query.filter_by(courseid=courseid).all()
        return render_template('challengelist.html', challenges=challenges, courseid=courseid, is_admin = is_admin)
    
# newChallenge = Challenge(challengeid='ooga booga', courseid='1050', description='put ooga in booga', difficulty='easy')
# newChallenge1 = Challenge(challengeid='oogity boogity', courseid='CS1050', description='Make an array of 10 boogities', difficulty='medium')
#db.session.add(newChallenge)
#db.session.add(newChallenge1)

    # newCourse = Course(courseid='CS1050', description='Computer Science 1')
    # newCourse1 = Course(courseid='CS1051', description='Computer Science 2')
    # newCourse2 = Course(courseid='CS1052', description='Computer Science 3')

    # db.session.add(newCourse)
    # db.session.add(newCourse1)
    # db.session.add(newCourse2)
    # newCourseOoga = Challenge(courseid = 'CS1050', challengeid='wortwort', description='Create function multiply that will multiply 2 numbers and return the result.', difficulty='HARD', test_cases=[TestCase(input="1,2", required_output='2', test_function='multiply'), TestCase(input="3,2", required_output='6', test_function='multiply')])
    # db.session.add(newCourseOoga)
    # db.session.commit()
    # If no specific courseid is provided, list all courses


    courses = Course.query.all()
    return render_template('courselist.html', courses=courses)

@app.route('/completed', methods=['GET', 'POST'])
@login_required
def completed():
    userchallenge = UserChallenge.query.filter_by(user_id=current_user.id).all()

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


@app.route('/addchallenge', methods=['GET', 'POST'])
#@login_required
def add_challenge():
    if not isinstance(current_user._get_current_object(), Admin):
        return redirect(url_for('user_profile'))
    cform = ChallengeForm()
    if cform.validate_on_submit():
        newChallenge = Challenge(challengeid=cform.challengeid.data,
                                 courseid=cform.courseid.data,
                                 description=cform.description.data,
                                 difficulty=cform.cform.data)
        for tcf in cform.test_cases:
            test_input = tcf.test_input.data
            expected_output = tcf.expected_output.data
            newTestCase = TestCase(challengeid=newChallenge.challengeid,  # or you can set the relationship directly
                               test_function=cform.functionName.data,  # You didn't mention this, you'll need to determine what goes here
                               input=test_input,
                               required_output=expected_output)
            db.session.add(newTestCase)
        db.session.add(newChallenge)
        db.session.commit()

    return render_template('addChallenge.html', form=cform)
