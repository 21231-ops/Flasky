# from flask import Flask, session, redirect, render_template, url_for,flash
# from flask_bootstrap import Bootstrap
# from flask_mail import Mail, Message
# from flask_moment import Moment
# from flask_script import Manager, Shell
# from flask_migrate import Migrate,MigrateCommand
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
# from flask_sqlalchemy import SQLAlchemy
# from threading import Thread
# import os
#
#
# basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__)
# app.debug = True
# app.config['SECRET_KEY'] = 'hard to guess string'
# app.config['SQLALCHEMY_DATABASE_URI'] = \
#     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER'] = 'smtp.qq.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
# app.config['FLASKY_ADMIN'] = 'ikhdvn@qq.com'
#
# mail = Mail(app)
# bootstrap = Bootstrap(app)
# moment = Moment(app)
# db=SQLAlchemy(app)
# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
#
# class NameForm(FlaskForm):
#     name = StringField('What is your name?', validators=[DataRequired()])
#     submit = SubmitField('Submit')
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role, mail=mail)
# manager.add_command("shell",Shell(make_context=make_shell_context))
#
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
# def send_email(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
#                   sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr
#
# @app.route("/", methods=['GET','POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.name.data).first()
#         if user is None:
#             user = User(username = form.name.data)
#             db.session.add(user)
#             session['known'] = False
#             if app.config['FLASKY_ADMIN']:
#                 send_email(app.config['FLASKY_ADMIN'], 'NEW User',
#                            'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index.html',
#                            form = form,name=session.get('name'),
#                            known = session.get('known', False))
#
#
# @app.route("/user/<name>")
# def user(name):
#     return render_template('user.html',name=name)
#
#
#
# if __name__ == '__main__':
#     manager.run()
# import random
# from datetime import datetime,timedelta
# num = ''.join(random.choices('0123456789', k=6))
# print(num)
# expire = datetime.utcnow() + timedelta(minutes=10)
# print(datetime.utcnow())
# print(expire)

def test():
    print("test函数运行")

print(test.__name__)

# ikhdvn@qq.com
# 13696754052@163.com
# 哪里调用的 verify_password这个自定义方法
# http --json --auth : GET http://127.0.0.1:5000/api/v1.0/posts/
#
