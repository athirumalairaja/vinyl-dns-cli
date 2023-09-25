import requests
import json
from . import configure as configure
from .signature import generate_aws_signature as generate_aws_signature

METHOD = 'GET'
BODY = {}

def get_zone_info(args):
    try:
        path = '/zones'
        index_url = ''.join([configure.URL, path])
        headers = generate_aws_signature.authorizer(index_url, args.access_key, args.secret_key, METHOD, path, BODY)
        response = requests.get(index_url, headers = headers)
        if response.status_code == 200:
            return json.loads(json.dumps(
                                            {
                                                "statusCode": response.status_code,
                                                "message": json.loads(response.text)
                                            }
                                        )
                            )
        else:
            return json.loads(json.dumps(
                                            {
                                                "statusCode": response.status_code,
                                                "message": json.loads(response.text)
                                            }
                                        )
                            )
    except Exception as e:
        return json.loads(json.dumps(
                                    {
                                        "statusCode": 500,
                                        "message": f"Exception has occurred with {e}",
                                    }
                                ))