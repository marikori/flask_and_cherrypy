'''
Created on Apr 29, 2018

@author: marikori
'''

from app_api import simple_data


class TaskError(Exception):
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)



class TaskNotFound(TaskError):
    pass



class BadRequest(TaskError):
    pass



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
            return self.tasks
        
        else:
            task = [task for task in self.tasks if task["id"] == task_id]
            
            if len(task) == 0:
                raise TaskNotFound("Not found - task id " + repr(task_id))
            
            return task[0]
    
    
    
    def create_task(self, request):
        
        if not request.json or not 'title' in request.json:
            raise BadRequest("Bad Request - missing required key title")
        
        task = {
            'id': self.tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
        }
        
        self.tasks.append(task)
        
        return task
    
    
    
    def update_task(self, request, task_id):
        
        task = [task for task in self.tasks if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound("Not found - task id " + repr(task_id))
        
        if not request.json:
            raise BadRequest("Bad Request - no data provided")
        
        if 'title' in request.json and type(request.json['title']) != str:
            raise BadRequest("Bad Request - title has to be string")
        
        if 'description' in request.json and type(request.json['description']) is not str:
            raise BadRequest("Bad Request - description has to be string")
        
        if 'done' in request.json and type(request.json['done']) is not bool:
            raise BadRequest("Bad Request - done has to be boolean")
        
        task[0]['title'] = request.json.get('title', task[0]['title'])
        task[0]['description'] = request.json.get('description', task[0]['description'])
        task[0]['done'] = request.json.get('done', task[0]['done'])
        
        return task[0]
    
    
    
    def delete_task(self, task_id):
        
        task = [task for task in self.tasks if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound("Not found - task id " + repr(task_id))
        
        self.tasks.remove(task[0])
        
        return True

