#users/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from CompanyWebApp.models import User

# LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('用户密码', validators=[DataRequired()])
    submit = SubmitField('登录')

# REGISTRATION FORM
class RegistrationForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(),Email()])
    username = StringField('用户名称', validators=[DataRequired()])
    password = PasswordField('用户密码', validators=[DataRequired(),EqualTo('pass_confirm', message='输入密码应相同')])
    pass_confirm = PasswordField('密码确认', validators=[DataRequired()])
    submit = SubmitField('提交注册')

    def check_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('邮箱已经被注册！')
    def check_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已经被使用！')

# UPDATE USER FORM
class UpdateUserForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(), Email()])
    username = StringField('用户名称', validators=[DataRequired()])
    department = StringField('部门')
    level = StringField('职位')
    admin = BooleanField('是否成为管理员')
    picture = FileField('更新用户图片', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('更新')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册！')
    
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被使用！')
