from wtforms import SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField, BooleanField
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError

from app.models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(),Length(1, 64), Email()])
        username = StringField('username', validators=[
            DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                  'Usernames must have only letters, '
                                                  'numbers, dots or underscores')])

        role = SelectField('Role', coerce=int)
        name = StringField('Real name', validators=[Length(0, 64)])
        location = StringField('Location', validators=[Length(0, 64)])
        about_me = TextAreaField('About me')
        submit = SubmitField('Submit')
        confirmed = BooleanField('Confirmed')

        def __init__(self, user, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.role.choices = [(role.id, role.name)
                                for role in Role.query.order_by(Role.name).all()]
            self.user = user

        def validate_email(self, field):
            if field.data != self.user.email and \
                    User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already registered.')

        def validate_username(self, field):
            if field.data != self.user.username and \
                    User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already in use')

class PostForm(FlaskForm):
    body = PageDownField("你想说点什么？", validators=[DataRequired()])
    submit = SubmitField('提交')

class CommentForm(FlaskForm):
    body = StringField('发表评论', validators=[DataRequired()])
    submit = SubmitField('提交')