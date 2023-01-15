from flask import render_template, redirect, request, url_for
from app.authentication import blueprint
from app.authentication.models import User as Users
from app.authentication.forms import LoginForm, CreateAccountForm
from app import db,login_manager
from flask_login import (
    current_user,
    login_user,
    logout_user
)

@blueprint.route('/register', methods=['GET'])
def register():
    """Register a new user"""

    create_account_form = CreateAccountForm(request.form)
    return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

      

@blueprint.route('/add/user', methods=['POST'])
def add_user():
    """Register a new user"""

    create_account_form = CreateAccountForm(request.form)
    username = request.form['username']
    email = request.form['email']

    # Check usename exists
    user = Users.query.filter_by(username=username).first()
    if user:
        return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

    # Check email exists
    user = Users.query.filter_by(email=email).first()
    if user:
        return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

    # else we can create the user
    user = Users(**request.form)
    db.session.add(user)
    db.session.commit()

    # Delete user from session
    logout_user()

    return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

 

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

