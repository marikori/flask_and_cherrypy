'''
Created on Apr 29, 2018

@author: marikori
'''

class AppData(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.tasks = [
            {
                'id': 1,
                'title': 'Buy groceries',
                'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
                'done': False
            },
            {
                'id': 2,
                'title': 'Play role',
                'description': 'Just be yourself, 007', 
                'done': False
            }
        ]
    
    
    def get_tasks(self):
        return self.tasks
    
    
    def append_task(self, task):
        task['id'] = self.tasks[-1]['id'] + 1
        self.tasks.append(task)
        return task
    
    
    def remove_task(self, task):
        self.tasks.remove(task)
        return True
