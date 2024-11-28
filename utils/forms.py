from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, Regexp
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密碼', validators=[DataRequired()])
    submit = SubmitField('登入')

class RegisterForm(FlaskForm):
    name = StringField('名稱', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('密碼', validators=[
        DataRequired(),
        Length(min=8, message='密碼長度至少 8 個字元'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])',
               message='密碼必須包含大小寫字母、數字及特殊符號')
    ])
    confirm_password = PasswordField('確認密碼', validators=[
        DataRequired(), EqualTo('password', message='密碼不一致')
    ])
    avatar = FileField('頭像')
    submit = SubmitField('註冊')

class EditProfileForm(FlaskForm):
    email = StringField('Email', render_kw={'readonly': True})
    name = StringField('名稱', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('新密碼', validators=[Optional(), Length(min=8, max=128)])
    avatar = FileField('頭像')
    submit = SubmitField('儲存')