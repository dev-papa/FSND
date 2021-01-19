import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    done @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"*": {"origins": "*"}})

    '''
    done @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,PUT,OPTIONS")
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            ret: Category = Category.query.all()
            categories = [category.format() for category in ret]
            cnt = len(categories)
            if cnt == 0:
                # I don't think it's good idea to return 404 if no record found.
                # Should return 200 as response has total_count field.
                # And `abort` invoke `HTTP Exception` so have to catch 404 error in `except` clause again.
                abort(404)

            res = ({
                'success': True,
                'data': categories,
                'total_count': cnt
            })
            return jsonify(res), 200
        except Exception as err:
            abort(err.code)
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions', methods=['GET'])
    def get_queries():
        try:
            page = request.args.get('page', 1, type=int)
            if page is None or page <= 0:
                page = 1
            offset_start = (page - 1) * QUESTIONS_PER_PAGE
            ret: Question = Question.query.order_by(Question.id).offset(offset_start).limit(10).all()
            questions = [q.format() for q in ret]
            cnt = len(questions)
            if cnt == 0:
                abort(404)

            res = {
                'success': 'true',
                'data': questions,
                'total_count': cnt
            }
            return jsonify(res), 200
        except Exception as err:
            print(err)
            abort(err.code)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/question/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        print(question_id)
        return jsonify({'success': 'true'}), 200

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({'success': False, 'message': 'not found', 'data': [], 'total_count': 0}), 404

    @app.errorhandler(422)
    def unprocessable(err):
        return jsonify({'success': False, 'message': 'unprocessable'}), 422

    @app.errorhandler(500)
    def internal_server_error(err):
        return jsonify({'success': False, 'message': err.name, 'detail': err.description}), err.code


    return app
