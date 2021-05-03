import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from dotenv import load_dotenv

load_dotenv()
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:'+os.getenv('DATABASE_PASSWORD')+'@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question={
            'question':'What is your name?',
            'answer':'ahmed',
            'category':1,
            'difficulty':1
        }

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
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])

    def test_get_valid_page_questions(self):
        res=self.client().get('/questions?page=1')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)   
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_for_requsting_pages_donot_exsist(self):
        res=self.client().get('/questions?page=1000')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)   
        self.assertEqual(data['message'], 'resource not found')  

    def test_delete_question(self):
        question =Question(question='What is your name?',answer='ahmed',difficulty=1,category=2)
        question.insert()
        ide=str(question.id)
        res = self.client().delete('/questions/'+ide)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_delete_question_failure(self):
        res = self.client().delete('/questions/200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')  

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_422_if_question_creation_fails(self):
        question={
            'question':'What is your name?',
            'answer':'ahmed',
            'category':'jnnj',
            'difficulty':1
        }
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)


        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)         

    def test_search(self):
        x = {'searchTerm':'what'}
        res = self.client().post('/questions/search',json=x)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)    

    def test_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_questions_by_category_failue(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')  

    def test_quiz(self):
        x ={"previous_questions": [], "quiz_category": {"type": "click", "id": 0}}

        res = self.client().post('/quizzes', json=x)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_taking_quiz_failure(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')      


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()