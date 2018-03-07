from flask import render_template, redirect, flash, url_for, request
from autofit_app import app, db
from .forms import LoginForm, RegistrationForm, ConstantsForm
from flask_login import current_user, login_user, logout_user, login_required
from autofit_app.models import User, Post
from werkzeug.urls import url_parse

from autofit.engine.tools import find_matches


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ConstantsForm()
    if form.validate_on_submit():
        print('got here')

        submitted = (form.A.data, form.B.data, form.C.data)
        results = find_matches(form.A.data, form.B.data, form.C.data)
        return render_template("results.html", title='Results', form=form,
                               results=results, submitted=submitted)
        return redirect(url_for('results'))

    return render_template("index.html",
                           title='Home Page',
                           form=form)

@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    form = ConstantsForm()

    return render_template("results.html", title='Results', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)