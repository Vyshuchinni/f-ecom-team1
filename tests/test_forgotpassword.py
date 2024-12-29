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

    def test_forgetpassword_form_empty_email(self):
        """Test submitting the form with an empty email field."""
        response = self.client.post('/forgetpassword', data={'email': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)  # Assuming this is the error message for empty email

    def test_forgetpassword_form_invalid_email(self):
        """Test submitting the form with an invalid email format."""
        response = self.client.post('/forgetpassword', data={'email': 'invalid-email'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email address.", response.data)  # Assuming this is the error message for invalid email


if __name__ == '__main__':
    unittest.main()
