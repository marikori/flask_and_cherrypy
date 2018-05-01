'''
Created on Apr 29, 2018

@author: marikori
'''

class AppData(object):
    '''
    classdocs
    '''
    tasks = [
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


    def __init__(self):
        '''
        Constructor
        '''
        