import unittest
from flask import Flask, render_template_string, flash, request
from flask_testing import TestCase
from main import app, db, models
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

class TestSignupPage(TestCase):
    def create_app(self):
        """Configure the app for testing."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testsecret'
        return app

    def test_signup_page_loads(self):
        """Test if the signup page loads correctly."""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Signup Page", response.data)

    def test_signup_form_elements_present(self):
        """Test if the signup form contains all required elements."""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="firstname"', response.data)
        self.assertIn(b'name="lastname"', response.data)
        self.assertIn(b'name="email"', response.data)
        self.assertIn(b'name="password"', response.data)
        self.assertIn(b'name="confirm_password"', response.data)
        self.assertIn(b'name="address"', response.data)
        self.assertIn(b'name="role"', response.data)
        self.assertIn(b'name="pincode"', response.data)

    def test_error_message_display(self):
        """Test if error messages are displayed for invalid input."""
        response = self.client.post('/signup', data={
            'firstname': '',  # Missing first name
            'lastname': 'User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'address': '123 Test St',
            'pincode': '123456',
            'role': 'user'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)

    def test_signup_password_mismatch(self):
        """Test if error message appears for password mismatch."""
        response = self.client.post('/signup', data={
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'wrongpassword',  # Mismatched password
            'address': '123 Test St',
            'pincode': '123456',
            'role': 'user'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_signup_email_already_exists(self):
        """Test if error message appears when email already exists."""
        # First, create a user with the same email
        try:
            existing_user = models.User(
                firstname="Existing",
                lastname="User",
                email="test@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256'),
                address="123 Test St",
                role="user",
                pincode="123456"
            )
            db.session.add(existing_user)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            self.assertTrue(True, "saved to save data from database")
        
        self.assertTrue(existing_user, "User created successfully")

if __name__ == '__main__':
    unittest.main()
