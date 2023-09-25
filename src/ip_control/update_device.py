import requests
import json
from vinyl import configure

METHOD = 'POST' 
def update_device(args, access_token, id, interface_id):
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
                                                "id": id,  
                                                "hostname": args.record_set_name,
                                                "description": "automation",
                                                "deviceType": "Virtual Service",
                                                "domainName": args.domain,
                                                "interfaces": [
                                                                {
                                                                    "addressType": ["Static"],
                                                                    "id": interface_id,
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