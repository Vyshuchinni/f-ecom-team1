import unittest
from flask_testing import TestCase
from flask import session
from app import create_app, db, models  # Assuming create_app initializes your Flask app
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

class TestForgetPassword(TestCase):
    def create_app(self):
        app = create_app(config_class="TestConfig")
        return app

    def setUp(self):
        db.create_all()

        # Create a test user
        try:
            user = models.User(
                firstname="Test",
                lastname="User",
                email="test@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256'),
                address="123 Test St",
                role="user",
                pincode="123456"
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_forgetpassword_page_loads(self):
        """Test if the forget password page loads correctly."""
        response = self.client.get('/forgetpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Forgot Password", response.data)


if __name__ == '__main__':
    unittest.main()
