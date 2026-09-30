import re
import sys
import unittest

from flask import url_for

from app import create_app, db
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('陌生人' in response.get_data(as_text=True))

    def test_register_and_login(self):
        response = self.client.post(url_for('auth.register'), data={
            'email':'ikhdvn@qq.com',
            'username':'ikhdvn',
            'password':'ikhdvn',
            'confirm_password': 'ikhdvn'
        })
        print(f"注册状态码: {response.status_code}", file=sys.stderr)
        print(f"注册响应: {response.get_data(as_text=True)[:300]}", file=sys.stderr)
        self.assertTrue(response.status_code == 302)

        response = self.client.post(url_for('auth.login'), data={
            'email':'ikhdvn@qq.com',
            'password':'ikhdvn',
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('确认你的账户' in data or '你还没有确认账号' in data)

        user = User.query.filter_by(email='ikhdvn@qq.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('账号激活成功！' in data)

        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('已退出登录' in data)