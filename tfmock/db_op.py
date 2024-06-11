import json
import os

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class Report:
    def __init__(self, db_config=None):
        self.db_config = db_config
        if self.db_config is not None:
            config_path = os.path.join(os.path.dirname(__file__), "config", f'{os.environ.get("env", "local")}.json')
            with open(config_path, 'r') as file:
                config_dict = json.load(file)

            self.measurement = "requests"
            org = config_dict.get("org")
            self.bucket = config_dict.get("bucket")

            client = InfluxDBClient(url=config_dict.get("url"), token=config_dict.get("token"), org=org)
            self.write_api = client.write_api(write_options=SYNCHRONOUS)

    def insert_metric(self, url, method, request_headers, request_payload, status, response_headers, response_payload):
        if self.db_config is not None:
            point = (
                Point("requests")
                .tag("url", url)
                .tag("method", method)
                .tag("status", status)
                .field("request_payload", request_payload)
                .field("request_headers", json.dumps(request_headers))
                .field("response_headers", json.dumps(response_headers))
                .field("response_payload", response_payload)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def insert_mocks(self, url, method, request_headers, request_payload, status, response_headers, response_payload):
        if self.db_config is not None:
            point = (
                Point("mocks")
                .tag("url", url)
                .tag("method", method)
                .tag("status", status)
                .field("request_payload", request_payload)
                .field("request_headers", json.dumps(request_headers))
                .field("response_headers", json.dumps(response_headers))
                .field("response_payload", response_payload)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
