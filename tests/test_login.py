import unittest
from flask import Flask, session,render_template_string, flash, request
from werkzeug.security import generate_password_hash
from flask_testing import TestCase
from app import create_app, db, models  # Assuming create_app initializes your Flask app
from sqlalchemy.exc import IntegrityError

class TestLogin(TestCase):
    def create_app(self):
        app = create_app(config_class="TestConfig")
        return app

    def setUp(self):
        db.create_all()

        # Create a test user
        hashed_password = generate_password_hash("password")
        try:
            user = models.User(
                firstname="Test",
                lastname="User",
                email="test@example.com",
                address="123 Test St",
                role="user",
                pincode="123456",
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login Page", response.data)
    
    def test_login(self):
        """Test user login."""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_empty_email_and_password(self):
        """Test submitting empty email and password."""
        response = self.client.post('/login', data={
            'email': '',
            'password': ''
        }, follow_redirects=True)

        # Check that the form validation fails
        self.assertIn(b'This field is required.', response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_when_authenticated(self):
        """Test that a user cannot access the login page if already logged in."""
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })

        # Try accessing the login page again
        response = self.client.get('/login', follow_redirects=True)

        # Check that the user is redirected to home page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)



if __name__ == '__main__':
    unittest.main()