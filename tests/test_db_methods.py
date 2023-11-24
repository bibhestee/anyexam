#!/usr/bin/env python3
import unittest


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ set up class before test """
        from api.models.db import Database
        cls.db = Database()

    def test_create_model(self):
        """ test if model is created successfully """
        from api.models.admin import Admin
        email = 'test@test.com'
        admin = self.db.create_model(Admin, email=email)
        self.assertIsInstance(admin, Admin)
        self.assertEqual(admin.email, email)


if __name__ == '__main__':
    unittest.main()