import os
import unittest
import json
from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:admin@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertTrue(len(data))

    # Questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertTrue(len(data))

    def test_get_questions_with_pagination(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertTrue(len(data))

    def test_get_questions_with_no_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['total_count'], 0)
        self.assertTrue(len(data))

    def test_get_questions_with_invalid_pagination0(self):
        res = self.client().get('/questions?page=0')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertTrue(len(data))

    def test_get_questions_with_negative_pagination(self):
        res = self.client().get('/questions?page=-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertTrue(len(data))


    def test_get_questions_with_char_pagination(self):
        res = self.client().get('/questions?page=a')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertTrue(len(data))

    def test_delete_question(self):
        # Question for delete
        try:
            q = Question(question='q', answer='a', category=1, difficulty=2)
            q.id = 30
            q.insert()
        except:
            pass

        res = self.client().delete('/question/30')
        self.assertEqual(res.status_code, 200)

    def test_post_question(self):
        body = {
            'question': 'xxx',
            'answer': 'yyy',
            'category': 1,
            'difficulty': 2
        }
        res = self.client().post('/question', json=body)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertGreaterEqual(len(data), 0)

    def test_get_questions_by_search_term(self):
        res = self.client().get('/questions/search?t=Taj')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertGreaterEqual(len(data), 0)

    def test_get_questions_by_category(self):
        res = self.client().get('/questions/category/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_count'])
        self.assertGreaterEqual(len(data), 0)

    def test_play_questions(self):
        res = self.client().post('/questions/play')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        # self.assertTrue(data['success'])
        # self.assertTrue(data['total_count'])
        # self.assertGreaterEqual(len(data), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
