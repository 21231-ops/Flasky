import re
import sys
import threading
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

from app import create_app, db
from app.models import Role, User, Post

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        import logging
        logger = logging.getLogger('werkzeug')
        logger.setLevel("ERROR")

        try:
            cls.client = webdriver.Firefox()
        except:
            cls.client = None
            print("Web browser not available")

        db.create_all()
        Role.insert_roles()
        User.generate_fake(10)
        Post.generate_fake(10)

        admin_role = Role.query.filter_by(permissions=0xff).first()
        admin = User(email='admin@qq.com',
                     username='admin', password='admin',
                     role=admin_role, confirmed=True)
        db.session.add(admin)
        db.session.commit()
        user_role = Role.query.filter_by(name='User').first()
        john = User(email='john@qq.com',
                    username='john',
                    password='cat',
                    role=user_role,
                    confirmed=True)
        db.session.add(john)
        db.session.commit()

        threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()
            cls.client.quit()

    def setUp(self):
        if not self.client:
            self.skipTest('Web 浏览器不可用')
        self.client.delete_all_cookies()

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        self.client.get('http://localhost:5000')
        self.assertTrue(re.search('你好,\s+陌生人！',
                                  self.client.page_source))

        self.client.find_element(By.LINK_TEXT, '登录').click()
        self.assertTrue('<h1>登录</h1>' in self.client.page_source)

        self.client.find_element(By.NAME, 'email').\
            send_keys('john@qq.com')
        self.client.find_element(By.NAME, 'password').send_keys('cat')
        self.client.find_element(By.NAME, 'submit').click()
        self.assertTrue(re.search('你好,\s+john！', self.client.page_source))

        self.client.	find_element(By.LINK_TEXT, '主页').click()
        for m in re.finditer(r'<h1[^>]*>(.*?)</h1>', self.client.page_source, re.DOTALL):
            print(f"h1 原文 = {m.group(1)!r}", file=sys.stderr)
        self.assertTrue('<h1>你好, john！</h1>' in self.client.page_source)