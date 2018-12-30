# coding = utf-8
from flask import render_template, redirect, url_for, request, flash
from flask.json import jsonify
from flask_login import login_user, logout_user

from blog import db
from blog.forms.auth import RegisterForm, LoginForm
from blog.helpers.common import redirect_back
from blog.models.user import User
from . import blog_bp


@blog_bp.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password1.data
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('blog.login',form=form))
    return render_template('auth/register.html', form=form)


@blog_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user.password == form.password.data:
            login_user(user, remember=True)
            return redirect_back()
        else:
            flash('用户名或密码错误',category='auth_error')
    if form.csrf_token.errors:
        flash('页面超时',category='auth_error')
    return render_template('auth/signin.html', form=form)


@blog_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect_back()


@blog_bp.route('/getuser/<int:uid>')
def get_user(uid):
    user = User.query.get(uid)
    o = dict(user)
    return jsonify(o)