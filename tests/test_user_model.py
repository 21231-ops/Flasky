import unittest
from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password = 'ikhdvn')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'ikhdvn')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'ikhdvn')
        self.assertTrue(u.verify_password('ikhdvn'))
        self.assertFalse(u.verify_password('cat'))

    def test_password_salts_are_random(self):
        u = User(password = 'ikhdvn')
        u2 = User(password = 'ikhdvn')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        db.session.commit()
        u = User(email='ikhdvn@qq.com', password='ikhdvn')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
