import logging
from concurrent.futures import ThreadPoolExecutor

from tfmock.cloud_services.azure.azure import AzureMocker
from tfmock.predict import predict
from tfmock.proxy.proxy2 import ProxyRequestHandler, ThreadingHTTPServer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


class SSLStripRequestHandler(ProxyRequestHandler):
    mock_func = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def request_handler(self, req, req_body):
        self.close_connection = True

        if self.mock_func is None:
            res = predict(req, req_body)
        else:
            res = self.mock_func(req, req_body)

        if res is not None:
            return res

    def response_handler(self, req, req_body, res, res_body):
        return


class MockServer:
    def __init__(self, mock_func, mock=True, port=8081):
        server_address = ('::1', port)
        SSLStripRequestHandler.protocol_version = "HTTP/1.1"
        SSLStripRequestHandler.mock_func = mock_func
        httpd = ThreadingHTTPServer(server_address, SSLStripRequestHandler)
        sa = httpd.socket.getsockname()
        logging.info(f"Serving HTTP Proxy on {sa[0]} {port} {sa[1]} ...")

        self.mock = mock
        self.httpd = httpd
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.executor.submit(self.start)

    def start(self):
        self.httpd.serve_forever()

    def close(self):
        self.httpd.shutdown()
        self.executor.shutdown(wait=False, cancel_futures=True)


if __name__ == '__main__':
    mocker = AzureMocker()
    MockServer(mock_func=mocker.mock_request)
