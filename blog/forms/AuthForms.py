from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import Models


class LoginForm(FlaskForm):
    email = StringField("Enter Email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField()


class RegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=2, max=30)])
    username = StringField("username", validators=[DataRequired(), Length(min=3, max=16)])
    email = StringField("Enter Email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    password_conformation = PasswordField("password again", validators=[DataRequired(), 
        EqualTo('password', message="password doesn't mach")])
    submit = SubmitField()

    def validate_email(self, email_field):
        if Models.User.query.filter_by(email=email_field.data).first():
            raise ValidationError("The email is already exists, reset password if needed.")

    def validate_username(self, username_field):
        if Models.User.query.filter_by(username=username_field.data).first():
            raise ValidationError("The username is already been used.")



class RequestResetForm(FlaskForm):
    email = StringField("Enter Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Get the password")  


    def validate_email(self, email_field):
        user = Models.User.query.filter_by(email=email_field.data).first()
        if user is None:
            raise ValidationError("No Email Exsists")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("new password", validators=[DataRequired()])
    password_conformation = PasswordField("password again", validators=[DataRequired(), 
        EqualTo('password', message="password doesn't mach")])
    submit = SubmitField("Reset the password")  