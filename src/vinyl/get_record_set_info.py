import requests
import json
from . import configure as configure
from .signature import generate_aws_signature as generate_aws_signature

METHOD = 'GET'

def get_record_set_info(args, zone_id):
    try:
        params = {'recordNameFilter': args.record_set_name}
        body = {}
        path = ''.join(['/zones/', zone_id,'/recordsets?', 'recordNameFilter=', args.record_set_name])
        index_url = ''.join([configure.URL, path])
        headers = generate_aws_signature.authorizer(index_url, args.access_key, args.secret_key, METHOD, path, body, params)
        response = requests.get(index_url, headers = headers)
        if response.status_code == 200:
            return json.loads(json.dumps(
                                            {
                                                "statusCode": response.status_code,
                                                "message": json.loads(response.text),
                                                "name":args.record_set_name,
                                                "domain":args.domain
                                            }
                                        )
                            )
        else:
            return json.loads(json.dumps(
                                            {
                                                "statusCode": response.status_code,
                                                "message": json.loads(response.text),
                                                "name":args.record_set_name,
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