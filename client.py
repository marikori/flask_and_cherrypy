#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: marikori
'''

from urllib.request import Request
from urllib.request import urlopen
import ssl, json, base64

ssl_context = ssl.create_default_context();
ssl_context.check_hostname=False
ssl_context.verify_mode=ssl.CERT_NONE



def call(uri, data = None, headrs = None, method = "GET"):
    
    print("REQUEST")
    print(method + " " + uri)
    print("headrs " + str(headrs))
    print("data " + str(data))
    
    try:
        if headrs is not None:
            request = Request(uri, data, headers = headrs, method = method)
        
        else:
            request = Request(uri, data, method = method)
        
        resp = urlopen(request, context = ssl_context)
    
    except Exception as e:
        if hasattr(e, "read"):
            print("EXCEPTION")
            print("code " + str(e.code))
            print(e.read().decode('utf-8'))
        
        raise e
    
    resp_json = json.loads(resp.read().decode('utf-8'))
    print("RESPONSE")
    print(json.dumps(resp_json, indent=4, sort_keys=True))
    print()
    
    return resp_json



if __name__ == '__main__':
    
    headrs = {'Content-Type' : 'application/json'}
    creds = "user007:python"
    headrs['Authorization'] = b"Basic " + base64.b64encode(creds.encode('ascii'))
    
    d1put = {"title": "blabla", "description": "bladesc", "done": False}
    
    #host = "http://localhost:5000"
    host = "https://localhost:8080"
    
    response = call(host + "/todo/api/v1.0/tasks", headrs = headrs)
    response = call(host + "/todo/api/v1.0/tasks", json.dumps(d1put).encode("utf-8"), headrs, method = "POST")
    response = call(host + "/todo/api/v1.0/tasks/3", json.dumps(d1put).encode("utf-8"), headrs, method = "PUT")
    response = call(host + "/todo/api/v1.0/tasks/1", headrs = headrs, method = "DELETE")
    response = call(host + "/todo/api/v1.0/tasks/2", headrs = headrs)
    response = call(host + "/todo/api/v1.0/tasks", headrs = headrs)
