#!/usr/bin/env python3
"""
Flask based RESTful API deployed on Cherrypy server.
"""

import cherrypy

from flask import Flask, jsonify, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

from app_api.simple_api import SimpleApi
from app_api.simple_data import AppData



app = Flask(__name__)
auth = HTTPBasicAuth()

app_data = AppData()
simple_api = SimpleApi(app_data)



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
    return jsonify({'task': make_public_task(simple_api.get_task(task_id))})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    return jsonify({'task': make_public_task(simple_api.create_task(request.json))}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    return jsonify({'task': make_public_task(simple_api.update_task(request.json, task_id))})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    return jsonify({'result': simple_api.delete_task(task_id)})


@app.errorhandler(Exception)
def app_excps(e):
    return make_response(jsonify({'error': str(e)}), e.code)


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




