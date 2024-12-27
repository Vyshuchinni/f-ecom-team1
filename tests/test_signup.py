import unittest
from flask import Flask, render_template_string, flash, request
from flask_testing import TestCase
from main import app, db, models
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

    def test_login_redirects_on_success(self):
        """Test if submitting the login form redirects on success."""
        response = self.client.post('/signup', data={
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'address': '123 Test St',
            'pincode': '123456',
            'role': 'user'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

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



if __name__ == '__main__':
    unittest.main()
