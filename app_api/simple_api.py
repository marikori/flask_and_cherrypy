"""Simple API for data manipulation."""

class TaskError(Exception):
    """Master class for simple api exceptions."""
    
    def __init__(self, message, code):
        """
        Args:
            message (str): Human readable string describing the exception.
            code (int): Error code.
        """
        self._code = code
        self._message = message

    @property
    def code(self):
        """int: Exception error code."""
        return self._code

    @property
    def message(self):
        """str: Human readable string describing the exception."""
        return self._message

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.message



class TaskNotFound(TaskError):
    """
    *404* `Not Found`.

    Raise if a task ID does not exist.
    """
    def __init__(self, task_id):
        """
        Args:
            task_id (int): Task ID which is not found.
        """
        super().__init__('Task ID {} not found.'.format(task_id), 404)



class BadRequest(TaskError):
    """
    *400* `Bad Request`

    Raise if the browser sends something to the application the application
    or server cannot handle.
    """    
    def __init__(self, message):
        """
        Args:
            message (str): Human readable string describing the exception.
        """
        super().__init__(message, 400)



class SimpleApi(object):
    """
    Implements Simple API.
    
    Application used for manipulating Tasks data.
    """

    def __init__(self, app_data):
        """
        Args:
            app_data (app_api.simple_data.AppData): Data manipulation object.
        
        Attributes:
            app_data (app_api.simple_data.AppData): Data manipulation object.
        """
        self.app_data = app_data
    
    
    
    def get_task(self, task_id):
        """
        Query database and return one task.
        
        Args
            task_id (int): Task ID of task to be returned.
        
        Returns:
            dict: Task.
            
        Raises:
            TaskNotFound: if task_id does not exist.
        """
        task = [task for task in self.app_data.get_tasks() if task["id"] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound(task_id)
        
        return task[0]
    
    
    
    def get_tasks(self):
        """
        Query tasks from database and return all tasks.
        
        Args:
            task_id (int: task ID of task to be returned. If None, return all tasks.
        Returns:
            list(disct): Tasks.
        """
        return self.app_data.get_tasks()
    
    
    
    def create_task(self, request):
        """
        Create / add new task into database.
        
        Args
            request (dict): Task to be added.
        
        Returns:
            dict: Task added to db.
            
        Raises:
            BadRequest: if request does not contain key with value 'title'.
        """
        if not request or not 'title' in request:
            raise BadRequest("Missing required key \'title\'")
        
        task = {
            'title': request['title'],
            'description': request.get('description', ""),
            'done': False
        }
        
        return self.app_data.append_task(task)
    
    
    
    def update_task(self, request, task_id):
        """
        Update existing task in database.
        
        Args
            task_id (int): ID of task to be updated.
            request (dict): Task data to be used for the update.
        
        Returns:
            dict: Updated task.
            
        Raises:
            TaskNotFound: if task_id does not exist.
            BadRequest: if
            * request['title'] is not string or
            * request['description'] is not string or
            * request['done'] is not boolean.
        """
        task = [task for task in self.app_data.get_tasks() if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound(task_id)
        
        if not request:
            raise BadRequest("No data provided")
        
        if 'title' in request and type(request['title']) != str:
            raise BadRequest("Title has to be string")
        
        if 'description' in request and type(request['description']) is not str:
            raise BadRequest("Description has to be string")
        
        if 'done' in request and type(request['done']) is not bool:
            raise BadRequest("Done has to be boolean")
        
        task[0]['title'] = request.get('title', task[0]['title'])
        task[0]['description'] = request.get('description', task[0]['description'])
        task[0]['done'] = request.get('done', task[0]['done'])
        
        return task[0]
    
    
    
    def delete_task(self, task_id):
        """
        Delete existing task from database.
        
        Args
            task_id (int): Task ID to be deleted.
        
        Returns:
            dict: Deleted task..
            
        Raises:
            TaskNotFound: if task_id does not exist.
        """
        task = [task for task in self.app_data.get_tasks() if task['id'] == task_id]
        
        if len(task) == 0:
            raise TaskNotFound(task_id)
        
        return self.app_data.remove_task(task[0])

