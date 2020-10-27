from flask import Flask, render_template, flash, redirect, request
from app.forms import LoginForm, RegistrationForm
from flask_login import LoginManager, current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.urls import url_parse
from app import app, db
import email_validator


@app.route('/')
def main():
    return render_template('index.html', title='Covert channels')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('user_page')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = 'user_page'
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('user_page')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('login')
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/user_page')
@login_required
def user_page():
    return render_template('user_page.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/types')
@login_required
def types():
    return render_template('types.html')


@app.route('/types/storage')
@login_required
def storage():
    return render_template('storage.html')


@app.route('/types/timing')
@login_required
def timing():
    return render_template('timing.html')


@app.route('/types/behavioral')
@login_required
def behavioral():
    return render_template('behavioral.html')


if __name__ == '__main__':
    app.run()
