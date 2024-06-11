import json
import logging

from .db_op import Report
from .predict import predict
from .proxy.proxy2 import ProxyRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# sample token
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Imk2bEdrM0ZaenhSY1ViMkMzbkVRN3N5SEpsWSJ9" \
               ".eyJhdWQiOiI2ZTc0MTcyYi1iZTU2LTQ4NDMtOWZmNC1lNjZhMzliYjEyZTMiLCJpc3MiOiJodHRwczovL2xvZ2" \
               "luLm1pY3Jvc29mdG9ubGluZS5jb20vNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3L3YyLjAiLCJpYX" \
               "QiOjE1MzcyMzEwNDgsIm5iZiI6MTUzNzIzMTA0OCwiZXhwIjoxNTM3MjM0OTQ4LCJhaW8iOiJBWFFBaS84SUFBQUF0QWFaTG8z" \
               "Q2hNaWY2S09udHRSQjdlQnE0L0RjY1F6amNKR3hQWXkvQzNqRGFOR3hYZDZ3TklJVkdSZ2hOUm53SjFsT2NBbk5aY2p2a295ckZ" \
               "4Q3R0djMzMTQwUmlvT0ZKNGJDQ0dWdW9DYWcxdU9UVDIyMjIyZ0h3TFBZUS91Zjc5UVgrMEtJaWpkcm1wNjlSY3R6bVE9PSIsImF6cC" \
               "I6IjZlNzQxNzJiLWJlNTYtNDg0My05ZmY0LWU2NmEzOWJiMTJlMyIsImF6cGFjciI6IjAiLCJuYW1lIjoiQWJlIExpbmNvbG4iLCJvaWQ" \
               "iOiI2OTAyMjJiZS1mZjFhLTRkNTYtYWJkMS03ZTRmN2QzOGU0NzQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmVsaUBtaWNyb3NvZnQuY29" \
               "tIiwicmgiOiJJIiwic2NwIjoiYWNjZXNzX2FzX3VzZXIiLCJzdWIiOiJIS1pwZmFIeVdhZGVPb3VZbGl0anJJLUtmZlRtMjIyWDVyclYzeERxZkt" \
               "RIiwidGlkIjoiNzJmOTg4YmYtODZmMS00MWFmLTkxYWItMmQ3Y2QwMTFkYjQ3IiwidXRpIjoiZnFpQnFYTFBqMGVRYTgyUy1JWUZBQSIsInZlciI6IjIuMCJ9.pj4N-w_3Us9DrBLfpCt"


class SSLStripRequestHandler(ProxyRequestHandler):
    mock_func = None
    db_config = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = Report(self.db_config)

    def request_handler(self, req, req_body):
        self.close_connection = True
        u = urlsplit(req.path)
        if u.path.startswith("/mock_msi"):
            return {
                'status': 200,
                'reason': 'created',
                'headers': {
                    "content-type": "application/json"
                },
                'res_body_plain': json.dumps({
                    "access_token": access_token,
                    "refresh_token": "",
                    "expires_in": "3599",
                    "expires_on": "1506484173",
                    "not_before": "1506480273",
                    "resource": "https://management.azure.com/",
                    "token_type": "Bearer"
                })
            }

        if self.mock_func is None:
            res = predict(req, req_body)
        else:
            res = self.mock_func(req, req_body)

        if res is not None:
            self.report.insert_mocks(url=req.path, method=req.command, request_headers=req.headers.items(),
                                     request_payload=req_body, status=res.code, response_headers=res.headers.items(),
                                     response_payload=res.body.decode("utf-8"))
            return res

    def response_handler(self, req, req_body, res, res_body):
        self.report.insert_metric(url=req.path, method=req.command, request_headers=req.headers.items(),
                                  request_payload=req_body, status=res.code, response_headers=res.headers.items(),
                                  response_payload=res_body.decode("utf-8"))
        return


class MockServer:
    def __init__(self, mock_func, db_config=None, mock=True, port=8081):
        server_address = ('::1', port)
        SSLStripRequestHandler.protocol_version = "HTTP/1.1"
        SSLStripRequestHandler.mock_func = mock_func
        SSLStripRequestHandler.db_config = db_config
        httpd = ThreadingHTTPServer(server_address, SSLStripRequestHandler)
        sa = httpd.socket.getsockname()
        logging.info(f"Serving HTTP Proxy on {sa[0]} {port} {sa[1]} ...")
        httpd.serve_forever()
        self.mock = mock
        self.httpd = httpd

    def close(self):
        self.httpd.server_close()


if __name__ == '__main__':
    MockServer()
