import json

def format_response(vinyl_code, ip_code, operation, args, ip_response=None):
    if vinyl_code == 202 and ip_code == 200:
      status_code = 202
    elif vinyl_code != 202:
      status_code = vinyl_code
    elif ip_code != 202:
      status_code = ip_code
    else:
      status_code = 500
    vinyl_response = {
                    202:f"Accepted - the {operation} is valid and has been accepted for processing",
                    400:"Bad Request - the Record Set being updated is not active",
                    401:"Unauthorized - The authentication information provided is invalid",
                    403:"Forbidden - The user does not have the access required to perform the action",
                    404:f"Not Found - RecordSet with name {args.record_set_name} doesn't exists in zone {args.domain}",
                    409:f"RecordSet with name {args.record_set_name} and ip address {args.record_set_ip} already exists in zone {args.domain}",
                    422:"Unprocessable Entity - Bad Filter",
                    500:"Internal Server Error",
                  }
    
    ip_control_response = {
                    200:f"OK - the {operation} IP control entry is successfull",
                    202:f"Accepted - the {operation} is valid and has been accepted for processing",
                    400:ip_response,
                    401:"Unauthorized - The authentication information provided is invalid",
                    403:"Forbidden - The user does not have the access required to perform the action",
                    404:f"No device found associated with {args.record_set_ip} in container null",
                    409:f"Entry with name {args.record_set_name} and ip address {args.record_set_ip} already exists in IP control",
                    500:"Internal Server Error",
                  }
    
    return json.loads(json.dumps(
                                    {
                                        "statusCode": status_code,
                                        "message": {"Vinyl" : vinyl_response[vinyl_code],
                                                    "IP control": ip_control_response[ip_code]},
                                        "name": args.record_set_name,
                                        "address": args.record_set_ip,
                                        "domain": args.domain
                                    }
                                )
                     )
                  
def alias_response(code, args, operation=None ):
    response = {  
                  200:f"OK - the {operation} alias is successfull",
                  202:f"Accepted - the {operation} is valid and has been accepted for processing",
                  400:"Bad Request - the record set or zone being updated is not active",
                  401:"Unauthorized - The authentication information provided is invalid",
                  403:"Forbidden - The user does not have the access required to perform the action",
                  404:f"Not Found - {args.alias} doesn't exist in zone {args.domain}",
                  409:f"The alias {args.alias} is already mapped with record set {args.record_set_name}",
                  422:"Unprocessable Entity",
                  500:"Internal Server Error",
                }

    return json.loads(json.dumps(
                                    {
                                        "statusCode": code,
                                        "message": response[code],
                                        "name": args.record_set_name,
                                        "alias": args.alias,
                                        "domain": args.domain
                                    }
                                )
                     )