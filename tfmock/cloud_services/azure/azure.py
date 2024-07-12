import logging
from urllib.parse import urlsplit

from tfmock.cloud_services.azure.services import list_mock_classes


class AzureMocker:
    def __init__(self):
        self.chains = []
        for name, service in list_mock_classes():
            for method_name in dir(service):
                if method_name.startswith('handle_'):
                    self.chains.append(eval(f'service().{method_name}'))

    def mock_request(self, req, req_body):
        urlmap = urlsplit(req.path)
        for chain in self.chains:
            res = chain(urlmap, req, req_body)
            if res is not None:
                return res

        logging.warning(f'fail process {req.command} {req.path}')

        return {
            'status': 200,
            'reason': 'created',
            'headers': {
                'content-type': 'application/json'
            },
            'body': {}
        }
