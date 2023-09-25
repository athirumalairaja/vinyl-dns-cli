import requests
import json
from vinyl import configure

METHOD = 'POST' 
def get_device(record_set_ip, access_token):
    try:
        path = ''.join(['/Gets/getDeviceByIPAddr','?ipAddress=', record_set_ip])
        index_url = ''.join([configure.IP_CONTROL_URL, path])
        headers = {
                'Authorization': ''.join(['Bearer ', access_token]),
                }
        payload={}
        response = requests.get(index_url, headers=headers, data = payload)
        return {"statusCode":response.status_code, "message":json.loads(response.text)}
    except Exception as e:
        print("Exception has occured with ", e)