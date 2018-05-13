"""Fake database handler for Flask Cherrypy POC purposes"""

class AppData(object):
    """Implements the demo database handler"""
    def __init__(self):
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
