import requests
import json
import string
import random

# base url
base_url = "https://api-pi.projectinclusion.in/"

# auth token
auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VyVHlwZUlkIjoiMyIsIlNjaG9vbElkIjoiMTY3Mjk2NiIsIkFkdmFuY2VTY3JlZW5pbmciOiIxIiwic3ViIjoiMjcwIiwianRpIjoiYWFmNDc1NGItMGZhYy00OWMzLWIxMTgtMGQzNjk3YWM3YmYxIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiVEVBQ0hFUiIsImV4cCI6MTc3NTY0MDE2MywiaXNzIjoiVGVzdC5jb20iLCJhdWQiOiJUZXN0LmNvbSJ9.SKuNp7-PkG_vjP8V9NOJfTT1hN80zTe7SeD4OU2tknk"

#getrequest
def get_request():
    url = base_url + "api/CertificateType"
    print("get url:", url)

    headers = {
        "Authorization": auth_token
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json response body:", json_str)

#postrequest
def post_request():
    url = base_url + "api/CertificateType"
    print("post url:", url)
    headers = {"Authorization": auth_token}
    data={
        "createdDate": "2026-03-24T10:03:58.448Z",
        "updatedDate": "2026-03-24T10:03:58.448Z",
        "createdBy": 0,
        "updatedBy": 0,
        "status": 0,
        "priority": 0,
        "name": "string",
        "code": "string",
        "prefix": "string",
        "translatedLanguage": "string"
    }
    response=requests.post(url,json=data, headers=headers)
    assert response.status_code==201
    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json response body:", json_str)


#call
#get_request()
post_request()