'''
Created on Apr 29, 2018

@author: marikori
'''

from app_api.simple_data import AppData


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
        self.app_data = AppData()
    
    
    
    def get_tasks(self, task_id = None):
        
        if task_id is None:
            return self.app_data.get_tasks()
        
        else:
            task = [task for task in self.app_data.get_tasks() if task["id"] == task_id]
            
            if len(task) == 0:
                raise TaskNotFound("Not found - task id " + repr(task_id))
            
            return task[0]
    
    
    
    def create_task(self, request):
        
        if not request or not 'title' in request:
            raise BadRequest("Bad Request - missing required key title")
        
        task = {
            'title': request['title'],
            'description': request.get('description', ""),
            'done': False
        }
        
        return self.app_data.append_task(task)
    
    
    
    def update_task(self, request, task_id):
        
        task = [task for task in self.app_data.get_tasks() if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound("Not found - task id " + repr(task_id))
        
        if not request:
            raise BadRequest("Bad Request - no data provided")
        
        if 'title' in request and type(request['title']) != str:
            raise BadRequest("Bad Request - title has to be string")
        
        if 'description' in request and type(request['description']) is not str:
            raise BadRequest("Bad Request - description has to be string")
        
        if 'done' in request and type(request['done']) is not bool:
            raise BadRequest("Bad Request - done has to be boolean")
        
        task[0]['title'] = request.get('title', task[0]['title'])
        task[0]['description'] = request.get('description', task[0]['description'])
        task[0]['done'] = request.get('done', task[0]['done'])
        
        return task[0]
    
    
    
    def delete_task(self, task_id):
        
        task = [task for task in self.app_data.get_tasks() if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound("Not found - task id " + repr(task_id))
        
        return self.app_data.remove_task(task[0])

