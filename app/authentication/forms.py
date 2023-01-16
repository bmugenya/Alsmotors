from wtforms import Form, BooleanField, StringField, validators, PasswordField


class LoginForm(Form):
    username = StringField('Email Address',[validators.Length(min=6, max=35)])
    password = PasswordField('Password')


class CreateAccountForm(Form):
    username = StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email Address',[validators.Length(min=6, max=35)])
    password = PasswordField('Password')


