import requests
import json
from . import configure as configure
from .signature import generate_aws_signature as generate_aws_signature

METHOD = 'GET'
BODY = {}
def search_alias(args):
    try:
        params = {'recordNameFilter': ''.join([args.alias, '.', args.domain, '*',]), 'type':'A'}
        path = ''.join(['/recordsets?', 'recordNameFilter=', args.alias, '.', args.domain, '*', '&type=A'])
        index_url = ''.join([configure.URL, path])
        headers = generate_aws_signature.authorizer(index_url, args.access_key, args.secret_key, METHOD, path, BODY, params)
        response = requests.get(index_url, headers = headers)
        if response.status_code == 200:
            return json.loads(json.dumps(
                                            {
                                                "statusCode": response.status_code,
                                                "message": json.loads(response.text),
                                                "name":args.alias,
                                                "domain":args.domain
                                            }
                                        )
                            )
        else:
            return json.loads(json.dumps(
                                            {
                                                "statusCode": response.status_code,
                                                "message": json.loads(response.text),
                                                "name":args.alias,
                                                "domain":args.domain
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
