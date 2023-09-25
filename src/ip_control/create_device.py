import requests
import json
from vinyl import configure

METHOD = 'POST' 
def create_device(args, access_token):
    try:
        path = '/Imports/importDevices'
        index_url = ''.join([configure.IP_CONTROL_URL, path])
        headers = {
                    'Authorization': ''.join(['Bearer ', access_token]),
                    'Content-Type': 'text/plain'
                  }
        payload=json.dumps(
                            {
                                    "inpDevice": {
                                                    "hostname": args.record_set_name,
                                                    "description": "automation",
                                                    "deviceType": "Virtual Service",
                                                    "domainName": args.domain,
                                                    "interfaces": [
                                                                    {
                                                                        "addressType": ["Static"],
                                                                        "name": "Default",
                                                                        "ipAddress": [args.record_set_ip]
                                                                    }
                                                                  ]
                                                 }
                            }
                          )
        response = requests.post(index_url, headers=headers, data=payload)
        return {"statusCode":response.status_code, "message":json.loads(response.text)}
    except Exception as e:
        print("Exception has occured with ", e)