from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, SubmitField, DateTimeField, BooleanField,
                     IntegerField, TextAreaField, SelectField, FieldList)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from root.models import User
from flask_login import current_user


class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This Username is already in use')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This Username is already in use')


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestPassword(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')


class UpdateUserDetails(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This Username is already in use')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This Username is already in use')


class UploadResume(FlaskForm):
    picture = FileField('Update Resume', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    submit = SubmitField('Upload')


class UpdateUserPersonalDetails(FlaskForm):
    name = StringField('Name', render_kw={"placeholder": "Name"})
    mobile = IntegerField('Mobile', render_kw={"placeholder": "Mobile"})
    phone = IntegerField('Mobile 2', render_kw={"placeholder": "Mobile 2"})
    dob = StringField('Date of Birth', render_kw={"placeholder": "Date of Birth"})
    address = StringField('Address', render_kw={"placeholder": "Address"})
    hobbies = StringField('Hobbies', render_kw={"placeholder": "Hobbies"})
    country = StringField('Country', render_kw={"placeholder": "Country"})
    city = StringField('City', render_kw={"placeholder": "City"})
    submit = SubmitField('Update')


class SearchUser(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('This Username not exists')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=0, max=240)])
    submit = SubmitField('Submit')


class ContactFrom(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class ResumeDetails(FlaskForm):
    category = SelectField('Category', choices=[(x, x) for x in ['Please Select Category',
                                                                 'EDUCATION',
                                                                 'PROFESSIONAL EXPERIENCE',
                                                                 'PROJECT WORK',
                                                                 'EXTRACURRICULAR ACTIVITY']], coerce=str)
    year = StringField('Year', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    sub_title = StringField('Sub Title', validators=[DataRequired()])
    body = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_category(self, category):
        if category.data == 'Please Select Category':
            raise ValidationError('Please select category')