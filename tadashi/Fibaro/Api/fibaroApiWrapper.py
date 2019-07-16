import os
import requests
from ..Exception.fibaroApiConnectionException import FibaroApiConnectionException


class FibaroApiWrapper:
    def __init__(self, ip=None, user=None, password=None):
        self._user = user
        self._password = password
        self._ip = ip
    
    def connect(self, ip=None, user=None, password=None):
        if ip is not None:
            self._ip = ip
        if self._ip is None:
            raise FibaroApiConnectionException('an ip is required to connection')
        
        if user is not None:
            self._user = user
        if self._user is None:
            raise FibaroApiConnectionException('a user is required to connection')
        
        if password is not None:
            self._password = password
        if self._password is None:
            raise FibaroApiConnectionException('a password is required to connection')
        
    def get(self, object):
        r = requests.get('http://' + str(self._ip) + '/api/' + str(object), auth=(str(self._user), str(self._password)))
        
        status_code = r.status_code
        if status_code == 200:
            return r.text
        else:
            raise FibaroApiConnectionException('Api responds code ' + str(status_code) + ' when attempt to get ' + str(object))
        
    def post(self, id, value):
        params = {'deviceID' : id, 'name' : value}   
        r = requests.get('http://' + str(self._ip) + '/api/callAction', params = params, auth=(str(self._user), str(self._password)))
    
    
    
    
