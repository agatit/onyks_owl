import json
from requests import get, put, post, delete

req = {"name": "module_sink_win"}
data = json.dumps(req)

url = 'http://localhost:5000/owlapi/projects(perspective_transform)/modules(module_sink_win)'

# response = put(url, data=json.dumps(data))
# response = put(url, data=data)
response = delete(url, data=data)
# response = post(url, data=json.dumps(data))
print(response.json())
# print(data)
