'''
Created on Apr 29, 2018

@author: marikori
'''

from flask import jsonify, abort

from app_api import simple_data


class SimpleApi(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.tasks = simple_data.AppData.tasks
    
    
    
    def get_tasks(self, task_id = None):
        
        if task_id is None:
            return jsonify({'tasks': self.tasks})
        
        else:
            task = [task for task in self.tasks if task["id"] == task_id]
            
            if len(task) == 0:
                abort(404)
            
            return jsonify({'task': task[0]})
    
    
    
    def create_task(self, request):
        
        if not request.json or not 'title' in request.json:
            abort(400)
        
        task = {
            'id': self.tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
        }
        
        self.tasks.append(task)
        
        return jsonify({'task': task}), 201
    
    
    def update_task(self, request, task_id):
        
        task = [task for task in self.tasks if task['id'] == task_id]
        
        if len(task) == 0:
            abort(404)
        
        if not request.json:
            abort(400)
        
        if 'title' in request.json and type(request.json['title']) != str:
            abort(400)
        
        if 'description' in request.json and type(request.json['description']) is not str:
            abort(400)
        
        if 'done' in request.json and type(request.json['done']) is not bool:
            abort(400)
        
        task[0]['title'] = request.json.get('title', task[0]['title'])
        task[0]['description'] = request.json.get('description', task[0]['description'])
        task[0]['done'] = request.json.get('done', task[0]['done'])
        
        return jsonify({'task': task[0]})

