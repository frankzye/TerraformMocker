import json
import re

from tfmock.db import Database


class VirtualMachineScaleSetMock:
    database = Database()

    def handle_vmss(self, urlmap, req, req_body):
        match = re.match(r'^/subscriptions/((\w|-)+)/resourceGroups/((\w|-)+)/providers/Microsoft.Compute/virtualMachineScaleSets/((\w|-)+)$', urlmap.path, re.IGNORECASE)
        if match is None:
            return

        res_id = urlmap.path
        name = res_id.split('/')[-1]

        if req.command == 'GET':
            if not self.database.exist(res_id):
                return {'status': 404, 'reason': '', 'headers': {}, 'body': {}}

            return {'status': 200, 'reason': '', 'headers': {'content-type': 'application/json'}, 'body': self.database.get(res_id)}

        if req.command == 'PUT' or req.command == 'PATCH':
            body = json.loads(req_body)
            self.database.save(res_id, {
                **body,
                'id': res_id,
                'name': name,
                'provisioningState': 'Succeeded'
            })
            return {'status': 200, 'reason': '', 'headers': {'content-type': 'application/json'}, 'body': self.database.get(res_id)}

        if req.command == 'DELETE':
            self.database.delete(res_id)
            return {'status': 200, 'reason': '', 'headers': {'content-type': 'application/json'}, 'body': {}}
