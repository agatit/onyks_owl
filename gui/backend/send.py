import json
from requests import get, put, post
data = json.load(open('data.json',))
# data = {"einz": 8}
url = 'http://localhost:5000/todos'

# response = put(url, data=json.dumps(data))
# response = put(url, data=data)
response = post(url, data=data)
# response = post(url, data=json.dumps(data))
print(response.json())
# print(data)

