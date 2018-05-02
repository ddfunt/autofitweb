from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from autofit_app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ConstantsForm(FlaskForm):
    A = FloatField('A (MHz)', validators=[DataRequired()])
    B = FloatField('B (MHz)', validators=[DataRequired()])
    C = FloatField('C (MHz)', validators=[DataRequired()])
    submit = SubmitField('Submit')
    #clear =

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.A.data = 6039.249
        self.B.data = 5804.909
        self.C.data = 2959.210