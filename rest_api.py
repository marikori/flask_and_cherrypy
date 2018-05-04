#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: marikori
'''

import cherrypy

from flask import Flask, jsonify, make_response, request, abort, url_for
from flask_httpauth import HTTPBasicAuth

from app_api.simple_api import SimpleApi, TaskNotFound, BadRequest



app = Flask(__name__)
auth = HTTPBasicAuth()

simple_api = SimpleApi()



def make_public_task(task):
    new_task = {}
    
    for field in task:
        
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        
        else:
            new_task[field] = task[field]
    
    return new_task



@auth.get_password
def get_password(username):
    if username == 'user007':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)



@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in simple_api.get_tasks()]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    try:
        return jsonify({'task': make_public_task(simple_api.get_tasks(task_id))})
    except TaskNotFound as e:
        abort(404, e.__str__())


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    try:
        return jsonify({'task': make_public_task(simple_api.create_task(request.json))}), 201
    except BadRequest as e:
        abort(400, e.__str__())


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    try:
        return jsonify({'task': make_public_task(simple_api.update_task(request.json, task_id))})
    except TaskNotFound as e:
        abort(404, e.__str__())
    except BadRequest as e:
        abort(400, e.__str__())


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    try:
        return jsonify({'result': simple_api.delete_task(task_id)})
    except TaskNotFound as e:
        abort(404, e.__str__())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error.description}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': error.description}), 400)


if __name__ == '__main__':
    #app.run(debug=True)
    # https://docs.cherrypy.org/en/latest/deploy.html
    cherrypy.tree.graft(app.wsgi_app, '/')
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            #'server.socket_port': 5000,
                            'server.ssl_module':'builtin',
                            'server.ssl_certificate':'cert/cert.pem',
                            'server.ssl_private_key':'cert/privkey.pem',
                            'engine.autoreload.on': False
                            })
    
    cherrypy.engine.start()




