"""Test for Simple API module"""
import unittest, copy
from unittest.mock import patch
from app_api.simple_data import AppData
from app_api.simple_api import SimpleApi, TaskNotFound, BadRequest


class TestSimpleApi(unittest.TestCase):
    
    def setUp(self):
        
        self.tasks = [
            {
                'id': 1,
                'title': 'Buy groceries',
                'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
                'done': False
            },
            {
                'id': 3,
                'title': 'test title',
                'description': 'test description', 
                'done': True
            },
            {
                'id': 4,
                'title': 'Play role',
                'description': 'Just be yourself, 007', 
                'done': False
            }
        ]
        
        self.request = {
            'title': 'new test task',
            'description': 'new test description', 
            'done': True
        }
        
        self.request_no_title = {
            'description': 'new test description', 
            'done': True
        }
        
        self.app_data = AppData()
        self.simple_api = SimpleApi()
    
    
    def tearDown(self):
        pass
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_get_tasks(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        self.assertListEqual(self.tasks, self.simple_api.get_tasks())
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_get_task_valid_id(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        self.assertDictEqual(self.tasks[1], self.simple_api.get_tasks(3))
    

    @patch('test.test_simple_api.AppData.get_tasks')
    def test_get_task_invalid_id(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        with self.assertRaises(TaskNotFound):
            self.simple_api.get_tasks(2)

    
    
    
    @patch('test.test_simple_api.AppData.append_task')
    def test_create_task(self, mock_append_task):
        mock_append_task.return_value = self.request
        self.assertDictEqual(self.request, self.simple_api.create_task(self.request))
    
    
    @patch('test.test_simple_api.AppData.append_task')
    def test_create_task_empty_request(self, mock_append_task):
        with self.assertRaises(BadRequest):
            self.simple_api.create_task(None)
    
    
    @patch('test.test_simple_api.AppData.append_task')
    def test_create_task_missing_title_request(self, mock_append_task):
        with self.assertRaises(BadRequest):
            self.simple_api.create_task(self.request_no_title)
    
    
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_update_task(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        ret_val = copy.deepcopy(self.request)
        
        ret_val["id"] = 1
        self.assertDictEqual(ret_val, self.simple_api.update_task(self.request, 1))
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_update_task_empty_request(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        with self.assertRaises(BadRequest):
            self.simple_api.update_task(None, 1)
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_update_task_invalid_id(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        with self.assertRaises(TaskNotFound):
            self.simple_api.update_task(self.request, 2)
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_create_task_title_wrong_type(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        
        self.request["title"] = 1
        with self.assertRaises(BadRequest):
            self.simple_api.update_task(self.request, 1)
        
        self.request["title"] = True
        with self.assertRaises(BadRequest):
            self.simple_api.update_task(self.request, 1)
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_create_task_description_wrong_type(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        
        self.request["description"] = 1
        with self.assertRaises(BadRequest):
            self.simple_api.update_task(self.request, 1)
        
        self.request["description"] = True
        with self.assertRaises(BadRequest):
            self.simple_api.update_task(self.request, 1)
    
    
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_create_task_done_wrong_type(self, mock_get_all_tasks):
        mock_get_all_tasks.return_value = self.tasks
        
        self.request["done"] = 1
        with self.assertRaises(BadRequest):
            self.simple_api.update_task(self.request, 1)
        
        self.request["done"] = "string"
        with self.assertRaises(BadRequest):
            self.simple_api.update_task(self.request, 1)
    
    
    
    
    @patch('test.test_simple_api.AppData.remove_task')
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_delete_task(self, mock_get_all_tasks, mock_remove_task):
        mock_get_all_tasks.return_value = self.tasks
        mock_remove_task.return_value = True
        self.assertTrue(self.simple_api.delete_task(1))
    
    
    @patch('test.test_simple_api.AppData.remove_task')
    @patch('test.test_simple_api.AppData.get_tasks')
    def test_delete_task_invalid_id(self, mock_get_all_tasks, mock_remove_task):
        mock_get_all_tasks.return_value = self.tasks
        mock_remove_task.return_value = False
        with self.assertRaises(TaskNotFound):
            self.simple_api.delete_task(2)



if __name__ == "__main__":
    unittest.main()