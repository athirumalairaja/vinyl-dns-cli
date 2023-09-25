import requests
import json
from . import configure as configure
from .signature import generate_aws_signature as generate_aws_signature

METHOD = 'DELETE'

def delete_record_set(args, zone_id, record_set_id):
    try:
        body = {}
        path = ''.join(['/zones/', zone_id,'/recordsets/', record_set_id])
        index_url = ''.join([configure.URL, path])
        headers = generate_aws_signature.authorizer(index_url, args.access_key, args.secret_key, METHOD, path, body)
        response = requests.delete(index_url, headers = headers)
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