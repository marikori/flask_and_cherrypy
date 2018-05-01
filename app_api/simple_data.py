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
            'title': 'Learn Python',
            'description': 'Need to find a good Python tutorial on the web', 
            'done': False
        }
    ]


    def __init__(self):
        '''
        Constructor
        '''
        