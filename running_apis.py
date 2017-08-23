import requests
import json

def post_list():
    '''
    test post a list
    '''
    ENDPOINT = "http://0.0.0.0:9050/lists"
    payload = {
       "budget": 44000,
    }
    res = requests.post(ENDPOINT, data=json.dumps(payload), headers={'content-Type': 'application/json'})
    print res.text
    #print res.status_code


def get_lists():

    ENDPOINT = "http://127.0.0.1:9050/lists"
    data = {}
    response = requests.get(ENDPOINT, params=data)
    print response.text


def put_lists():
    '''
    test put a list
    '''
    ENDPOINT = "http://0.0.0.0:9050/lists/{}"
    payload = {
       "name" : "independence",
       "budget": 55000,
    }
    res = requests.put(ENDPOINT.format(6), data=json.dumps(payload), headers={'content-Type': 'application/json'})
    #print res.text
    print res.status_code

#post_list()
#get_lists()
put_lists()

