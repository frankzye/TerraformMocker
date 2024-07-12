import importlib
import inspect
import os

ms = []

for file in os.listdir(os.path.dirname(__file__)):
    mod_name = file[:-3]
    if not mod_name.startswith('__'):
        ms.append(importlib.import_module(f'.{mod_name}', 'cloud_services.azure.services'))


def list_mock_classes():
    for m in ms:
        for name, cls in inspect.getmembers(m):
            if not name.startswith('__') and inspect.isclass(cls):
                yield name, cls
