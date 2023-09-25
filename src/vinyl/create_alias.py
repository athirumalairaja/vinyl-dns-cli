import requests
import json
from . import configure as configure
from .signature import generate_aws_signature as generate_aws_signature
from .get_zone_info import get_zone_info

METHOD = 'POST'

def create_alias(args, zone_id):
    try:
        record_owner = get_zone_info(args)['message']['zones'][0]['adminGroupId']
        body  = json.dumps(
                            {
                                "name": args.alias,
                                "type": "CNAME",
                                "ttl": 1200,
                                "records": [
                                    {
                                    "cname": ''.join([args.record_set_name, '.', args.domain])
                                    }
                                ],
                                "zoneId": zone_id,
                                "ownerGroupId": record_owner,
                                "fqdn": ''.join([args.alias, '.', args.domain]),
                                "zoneName": args.domain
                            }
                          )
        path = ''.join(['/zones/', zone_id,'/recordsets'])
        index_url = ''.join([configure.URL, path])
        headers = generate_aws_signature.authorizer(index_url, args.access_key, args.secret_key, METHOD, path, body)
        headers['X-Amz-Content-Sha256'] = configure.X_AMZ_CONTENT_SHA256
        headers['Content-Type'] = configure.CONTENT_TYPE

        response = requests.post(index_url, headers = headers, data = body)
        return {
            "statusCode" : response.status_code, 
            "message"    : json.loads(response.text)
        }
    except Exception as e:
        return json.loads(json.dumps(
                                    {
                                        "statusCode": 500,
                                        "message": f"Exception has occurred with {e}",
                                    }
                                ))
