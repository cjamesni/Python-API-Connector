from __future__ import absolute_import

import os
import logging
import ldap
import ldapurl
import json
import errno
import csv
import cStringIO
import codecs
import glob

from ldap.controls import SimplePagedResultsControl
from lib.connector import AssetsConnector
from lib.error import ConfigError


LOGGER = logging.getLogger("connectors/json_assets")  # pylint:disable=invalid-name


class Connector(AssetsConnector):
    MappingName = 'JSON-assets'
    Settings = {
        'directory':   {'order': 1, 'example': "/Users/daniel/Documents/development/Oomnitza/Connector/test_data"},
    }

    FieldMappings = {
    }

    def __init__(self, section, settings):
        super(Connector, self).__init__(section, settings)

        self._directory = os.path.abspath(self.settings.get('directory'))

    def authenticate(self):
        pass

    def do_test_connection(self, options):
        if os.path.isdir(self._directory):
            return {'result': True, 'error': ''}
        return {'result': False, 'error': '%r is not a directory.' % self._directory}

    def _load_records(self, options):
        for filename in glob.glob(os.path.join(self._directory, '*.json')):
            with open(filename, 'rb') as input_file:
                LOGGER.info("Processing input file: %s", filename)
                input_data = json.load(input_file)

                if isinstance(input_data, list):
                    for index, asset in enumerate(input_data):
                        if not isinstance(asset, dict):
                            raise Exception("List item #%s is not an object!" % index)
                        yield asset
                elif isinstance(input_data, dict):
                    yield input_data
                else:
                    raise Exception("File %r does not contain a list or object." % filename)
        else:
            LOGGER.info("No data files processed.")


