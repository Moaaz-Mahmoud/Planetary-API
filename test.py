import unittest
from app import app, db, Planet


class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_planets_route(self):
        # Assuming you have seeded some data in the test database
        response = self.client.get('/planets')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)


if __name__ == '__main__':
    unittest.main()
