import os.path
import pathlib

from setuptools import setup

root_folder = os.path.dirname(__file__)
long_description = pathlib.Path(os.path.join(root_folder, "readme.md")).read_text()

setup(
    name='tfmock',
    version='0.0.9',
    install_requires=[],
    packages=['tfmock'],
    package_data={
        '': ['config/*', 'proxy/*', 'cloud_services/*', 'cloud_services/azure/*', 'cloud_services/azure/services/*']
    },
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
