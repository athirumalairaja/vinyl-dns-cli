import requests
import json
from vinyl import configure
from urllib.parse import quote_plus

METHOD = 'POST'
def login(args):
    try:
        path = '/login'
        index_url = ''.join([configure.IP_CONTROL_URL, path])
        headers = {
                    'Content-Type': 'application/x-www-form-urlencoded' 
                  }
        payload=''.join(['username=', args.ipcontrol_username, '&password=', quote_plus(args.ipcontrol_password, safe="*")])
        response = requests.post(index_url, headers=headers, data = payload )
        return {"statusCode":response.status_code, "message":json.loads(response.text)}
    except Exception as e:
        print("Exception has occured with ", e)