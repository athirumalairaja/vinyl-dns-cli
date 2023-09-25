import boto3
from vinyl import configure
from urllib.parse import urljoin
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.compat import HTTPHeaders

from datetime import datetime
now = datetime.utcnow()

headers = {u'X-Amz-Date': now.strftime(u'%Y%m%dT%H%M%SZ')}

class AwsSigV4RequestSigner(object):
    def __init__(self, index_url: str, access_key: str, secret_access_key: str):
        self.url = index_url
        self.boto_session = boto3.Session(
            region_name=configure.REGION_NAME,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key)

    def sign_request_headers(self, method: str, path: str, headers: dict, body: str, params: object = None) -> HTTPHeaders:
        """
        Construct the request headers, including the signature

        :param method: The HTTP method
        :param path:  The URL path
        :param headers: The request headers
        :param body: The request body
        :param params: The query parameters
        :return:
        """
        request = AWSRequest(method=method, url=urljoin(self.url, path), auth_path=path, data=body, params=params, headers=headers)
        SigV4Auth(self.boto_session.get_credentials(), configure.SERVICE_NAME, configure.REGION_NAME).add_auth(request)
        return request.headers

def authorizer(url, akey, skey, method, path, body, params=None):
    auth = AwsSigV4RequestSigner(url,akey,skey)
    signature = auth.sign_request_headers(method, path, headers, body, params)
    return signature