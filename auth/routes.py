from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User
from utils.forms import RegisterForm, LoginForm
from utils.gcs import gcs_helper
from auth import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash('Email 已被註冊', 'danger')
            return redirect(url_for('auth.register'))

        # Handle avatar upload to GCS
        avatar_url = None
        if form.avatar.data:
            try:
                avatar_url = gcs_helper.upload_file(form.avatar.data, folder="avatars")
            except Exception as e:
                flash(f'頭像上傳失敗：{str(e)}', 'danger')
                return redirect(url_for('auth.register'))

        # Create a new user
        user = User(name=name, email=email, avatar=avatar_url)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('註冊成功，請登入', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('登入成功', 'success')
            return redirect(url_for('index'))
        flash('無效的 email 或密碼', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'info')
    return redirect(url_for('auth.login'))
