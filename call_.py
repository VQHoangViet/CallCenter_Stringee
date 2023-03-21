from imports import *
import json
# stringee server
url = 'https://api.stringee.com/v1/call2/callout'
token = 'eyJjdHkiOiJzdHJpbmdlZS1hcGk7dj0xIiwidHlwIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJqdGkiOiJTSy4wLmpaWnVNdjZ2Vkl5RmZZQVl4dlc3YWlnY2hmVDNiQUtjLTE2Nzg3MDA3MTUiLCJpc3MiOiJTSy4wLmpaWnVNdjZ2Vkl5RmZZQVl4dlc3YWlnY2hmVDNiQUtjIiwiZXhwIjoxNjgxMjkyNzE1LCJyZXN0X2FwaSI6dHJ1ZX0.z1TtVWF3tuB5QcLzw0mTgj3zMdYZ3zEITDUISp2uL6A'

# header
headers = {
    'Content-Type': 'application/json',
    'X-STRINGEE-AUTH': token # will be expired in 30 days
}

def build_body(from_, to_):
    body = {
    
            "from": {
                "type": "external", 
                "number": from_, # example: 842473001571
                "alias": from_
            },
            "to": [{
                "type": "external",
                "number": to_, # example: 84901144295
                "alias": to_
            }],
            "actions": [
            {    
                "action": "record",
                "eventUrl": "http://v2.stringee.com:8282/project_event_url",
                "format": "mp3",
            },
            {
                "action": "talk",
                "text": "Alo! Đây có phải số điện thoại của anh A không ạ?",
                
            }],
            "record": True,}
        

    return body

def outbound_call(from_, to_):
    body = build_body(from_, to_)
    response = requests.post(url, headers=headers, json=body)
    return response

# get call log from stringee
def get_call_log():
    res = requests.get('https://api.stringee.com/v1/call/log?limit=1000',headers=headers)
    return pd.json_normalize(res.json()['data']['calls'])
