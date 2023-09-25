import requests
import json
from vinyl import configure

METHOD = 'DELETE' 
def delete_device(args, access_token):
    try:
        path = '/Deletes/deleteDevice'
        index_url = ''.join([configure.IP_CONTROL_URL, path])
        headers = {
                    'Authorization': ''.join(['Bearer ', access_token]),
                    'Content-Type': 'text/plain'
                  }
        payload=json.dumps({
                                "inpDev": {
                                            "ipAddress": args.record_set_ip
                                        }
                            })
        response = requests.delete(index_url, headers=headers, data = payload)
        return {"statusCode":response.status_code, "message":json.loads(response.text)}
    except Exception as e:
        print("Exception has occured with ", e)