import requests
import json

response = requests.get("http://192.168.16.116:8000/uv")

uvresponse = []

def jprint(obj):
    text = json.dumps(obj, sort_keys=True)
    global uvresponse 
    uvresponse = text

jprint(response.json())

uv_index = uvresponse[14]
uv_lux = uvresponse[31+14],uvresponse[31+15]
print(uv_index)
print(uv_lux)