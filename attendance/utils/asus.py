import requests
from base64 import b64encode
from django.conf import settings


class Client:
    def __init__(self, data):
        self.mac = data.get('mac')
        self.ip = data.get('ip')
        self.interface = data.get('interface', 'wired')
        self.rssi = data.get('rssi')
        self.name = data.get('name')
        self.alias = data.get('alias')


class AsusRouter:

    _USER_AGENT = 'asusrouter-Android-DUTUtil-1.0.0.3.58-163'

    _CONTENT_TYPE = 'application/x-www-form-urlencoded'

    def __init__(self):
        self._session = requests.Session()
        self._url = f"https://{settings.ROUTER_IP}"
        self._username = settings.ROUTER_USERNAME
        self._password = settings.ROUTER_PASSWORD

        self.authenticate()

    def request(self, method, path, data=None):
        return self._session.request(
            method=method.upper(),
            url=self._url + path,
            headers={
                'User-Agent': self._USER_AGENT,
                'Content-Type': self._CONTENT_TYPE
            },
            data=data,
            verify=False
        )

    def get(self, payload):
        response = self.request('POST', '/appGet.cgi', {'hook': payload})
        return response.json()

    def authenticate(self):
        self.request(
            'POST',
            '/login.cgi',
            {
                'login_authorization': b64encode(
                    ('%s:%s' % (self._username, self._password)).encode('utf-8')
                ).decode('utf-8')
            }
        )

    def get_online_clients(self):
        response = self.get(
            'get_clientlist(appobj);wl_sta_list_2g(appobj);wl_sta_list_5g(appobj);wl_sta_list_5g_2(appobj);nvram_get(custom_clientlist)'
        )

        clients = response.get('get_clientlist', {})
        clients.pop('maclist', None)
        clients = list(clients.values())

        onlineClients = []
        for c in clients:
            if 'isOnline' in c and c['isOnline'] == '1':
                onlineClients.append({
                    'mac': c['mac'],
                    'ip': c['ip'],
                    'name': c['name']
                })
        return onlineClients


__all__ = [
    'AsusRouter'
]
