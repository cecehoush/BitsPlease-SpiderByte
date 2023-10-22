from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, Form, StringField, PasswordField, TextAreaField, DateField, SubmitField, validators, SelectField, IntegerField, FormField, FieldList
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class TestCaseForm(Form):
    test_input = StringField('Test Case', validators=[DataRequired()])
    expected_output = StringField('Expected Output', validators=[DataRequired()])

class ChallengeForm(FlaskForm):
    courseid = StringField('Course ID', validators=[DataRequired()])
    challengeid = StringField('Challenge Name', validators=[DataRequired()])
    description = TextAreaField('Challenge Description', validators=[DataRequired()])
    difficulty = StringField('Difficulty Level', validators=[DataRequired()])
    functionName = StringField('Function Name', validators=[DataRequired()])
    test_cases = FieldList(FormField(TestCaseForm), min_entries=1) # At least one test case
    submit = SubmitField('Submit')