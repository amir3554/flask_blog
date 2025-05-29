from flask import render_template, request
from blog.forms.AuthForms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from blog.models.AuthModels import User, StripeCustomer
from blog import db, bcrypt
from blog.utils.AuthUtils import send_reset_pwd_email
from flask import redirect, url_for, render_template, flash
from flask_login import login_user ,login_required, logout_user, current_user
from flask_paginate import Pagination


def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('MainRoute.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user is not None) and (bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            flash("Successfull Login", "success")
            return redirect(request.args.get('next') or url_for('MainRoute.home'))
        
        flash("Invalid email or password, please try again or make an account.", 'danger')
        return redirect(url_for('AuthRoute.user_login'))
    
    return render_template("auth/login.html", form=form, title="Login")


def user_register():    
    if current_user.is_authenticated:
        return redirect(url_for('MainRoute.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            )
        db.session.add(user)
        db.session.commit()
        flash(f"Register Was Success, Welcome {form.username.data}", "success")
        return redirect(url_for('AuthRoute.user_login'))
    
    return render_template('auth/register.html', form=form, title="Register")


@login_required
def user_logout():
    logout_user()
    flash("Loged out successfully", "success")
    return redirect(url_for("MainRoute.home"))




def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('MainRoute.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_pwd_email(user)
        flash("An email has been s ent for reseting password", "info")
        return redirect(url_for('AuthRoute.user_login'))

    return render_template('auth/reset_request.html', title="reset password", form=form)


def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('MainRoute.home'))  
    user = User.verify_reset_pwd_token(token)
    if user is None:
        flash("The link is expired, maybe try again.", "warinig")
        return redirect(url_for("AuthRoute.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')    #type:ignore
        db.session.commit()
        flash("password successfully reset", "success")
        return redirect(url_for('AuthRoute.user_login'))
    return render_template("auth/reset_password.html", title="Reset Password", form=form)


@login_required
def user_account():
    if current_user.is_admin:
        pagination = Pagination(total=len(current_user.articles))
        return render_template('auth/account.html', pagination=pagination)
    
    customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
    if customer is not None and customer.subscription_id:
        title=f"Hello {current_user.username}"
        return render_template('auth/account.html', title=title, customer=customer)
    else:
        return render_template('auth/account.html')


