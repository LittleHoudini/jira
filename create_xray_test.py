
import requests
from data import xray_json_template,template
from auth import  xray_auth_token
import json
from datetime import datetime

post_api_url = 'https://xray.cloud.getxray.app/api/v1/import/execution'
# Create the headers for the request
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {xray_auth_token}'
}


response = requests.post(
    post_api_url,
    headers=headers,
    json=xray_json_template,
)


# Print the response
print(json.dumps(response.json(), indent=4))

def create_xray_test(status,summary, steps,test_key=None):
    res = template
    res["tests"][0]["status"] = status
    if test_key is not None:
        res["tests"][0]["testKey"] = test_key
    res["tests"][0]["testInfo"]["summary"] = summary
    res["tests"][0]["testInfo"]["steps"] = steps
    response = requests.post(
        post_api_url,
        headers=headers,
        json=res,
    )

    return response.json()
    
    
def create_xray_template(status,summary, steps,test_key=None):
    template["tests"][0]["status"] = status
    if test_key is not None:
        template["tests"][0]["testKey"] = test_key
    template["tests"][0]["testInfo"]["summary"] = summary
    template["tests"][0]["testInfo"]["steps"] = steps
    return template

def post_test_result(status,summary, steps,test_key=None):
    result = create_xray_template(status,summary, steps,test_key)
    response = requests.post(
        post_api_url,
        headers=headers,
        json=result,
    )
    return response.json()