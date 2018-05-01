#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: marikori
'''

from flask import Flask, jsonify, make_response, request
from app_api.simple_api import SimpleApi


app = Flask(__name__)
simple_api = SimpleApi()


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return simple_api.get_tasks()


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    return simple_api.get_tasks(task_id)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    return simple_api.create_task(request)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
