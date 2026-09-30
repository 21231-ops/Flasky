from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .. models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z0-9_.]*$', 0,
                                              '只能包含字母、数字、下划线或点号')])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(),
        EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册。')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用。')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired()])
    confirm_new_password = PasswordField('确认新密码', validators=[DataRequired(),
        EqualTo('new_password', message='两次输入的新密码不一致')])
    submit = SubmitField('修改密码')

class ChangeEmailForm(FlaskForm):
    new_email = StringField('新邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('修改邮箱')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('新密码', validators=[DataRequired()])
    confirm_new_password = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('new_password', message='两次输入的新密码不一致')
    ])
    submit = SubmitField('重置密码')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('发送重置邮件')

class PasswordResetCodeForm(FlaskForm):
    code = StringField('验证码', validators=[DataRequired(), Length(6,6)])
    new_password = PasswordField('新密码', validators=[DataRequired()])
    confirm_new_password = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('new_password', message='两次输入的新密码不一致')
    ])
    submit = SubmitField('重置密码')