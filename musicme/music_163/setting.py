import sys
import json


class Setting(dict):
    _conf = {}

    def from_file(slef, path):
        with open(path, 'rb') as f:
            slef._conf = json.load(f)

    @property
    def mariadb_info(self):
        return (self._conf['db']['mariadb']['host'],
                self._conf['db']['mariadb']['port'],
                self._conf['db']['mariadb']['user'],
                self._conf['db']['mariadb']['password'])

    @property
    def miniodb_info(self):
        endpoint = '{}:{}'.format(self._conf['db']['minio']['host'],
                                  self._conf['db']['minio']['port'])
        return (endpoint,
                self._conf['db']['minio']['user'],
                self._conf['db']['minio']['password'])

    @property
    def proxy_path(self):
        return self._conf['tools']['proxy_server']
    
    @property
    def driver_path(self):
        return self._conf['tools']['edge_driver_path']