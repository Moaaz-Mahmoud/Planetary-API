import unittest
from app import app, db, User, Planet


class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planets_test.db'  # Use a separate testing database file
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        db.create_all()  # Create the database tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Drop the tables
        self.app_context.pop()

    def test_planets_route(self):
        # Assuming you have seeded some data in the test database
        response = self.client.get('/planets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_register_user(self):
        # Test registering a new user
        response = self.client.post('/register', data={
            'first_name': 'Meower',
            'last_name': 'Cat',
            'email': 'meower.cat@horses.com',
            'password': 'secure_password'
        })
        self.assertEqual(response.status_code, 201)  # Expect HTTP status code 201 (Created)
        self.assertEqual(response.json, {'message': 'User created successfully'})

    def test_register_existing_user(self):
        # Seed a user with the same email in the database
        existing_user = User(
            first_name='Meowish',
            last_name='Coder',
            email='meowish.coder@horses.com',
            password='secure_password'
        )
        db.session.add(existing_user)
        # db.session.commit()

        # Test registering a user with an existing email
        response = self.client.post('/register', data={
            'first_name': 'Meowful',
            'last_name': 'Designer',
            'email': 'meowish.coder@horses.com',  # Email already exists in the database
            'password': 'another_secure_password'
        })
        self.assertEqual(response.status_code, 409)  # Expect HTTP status code 409 (Conflict)
        self.assertEqual(response.json, {'message': 'The email already exists.'})


if __name__ == '__main__':
    unittest.main()