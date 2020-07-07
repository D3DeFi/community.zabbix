
# Will use ZabbixBase instead of object
class HostInterface(object):

    def __init__(self, **kwargs):
        self._zbx_api_version = 5.0  # example purposes
        try:
            self.hostid = kwargs['hostid']
            self.interfaceid = 123  # missing for new, lookup for existing, but how?
            self.type = kwargs['type']
            self.main = kwargs.get('main', False)
            self.useip = kwargs.get('useip', False)
            self.ip = kwargs.get('ip', '')
            self.dns = kwargs.get('ip', '')
            self.port = kwargs.get('port') or self._load_default_port(kwargs['type'])

            if self.type == 'snmp':
                if self._zbx_api_version <= 4.4:
                    self.bulk = True
                else:
                    self.defails = self._construct_snmp_details(kwargs.get('details', {}))
        except KeyError as e:
            # self._module.fail_json(msg='Failed to construct Host Interface. Error %s' % e)
            raise Exception('Failed to construct Host Interface. Error %s' % e)

    def _construct_snmp_details(self, details):
        if not details:
            return {}

        try:
            _params = {
                'version': details['version'],
                'bulk': details.get('bulk', True),
            }

            if _params['version'] == 'SNMPv3':
                _params.update({
                    'securityname': details.get('securityname', ''),  # mb required - dont remember
                    'securitylevel': details.get('securitylevel', 'noAuthNoPriv'),
                    'authpassphrase': details.get('authpassphrase', ''),  # mb required with AuthPriv
                    'privpassphrase': details.get('privpassphrase', ''),  # mb required with AuthNoPriv and AuthPriv
                    'authprotocol': details.get('authprotocol', 'MD5'),
                    'privprotocol': details.get('authprotocol', 'AES'),
                    'contextname': details.get('contextname', '')  #mb required
                })
            else:
                _params.update({'community': details['community']})

            return _params
        except KeyError as e:
            # self._module.fail_json(msg='Failed to construct SNMP details for Host Interface. Error %s' % e)
            raise Exception('Failed to construct SNMP details for Host Interface. Error %s' % e)

    def _load_default_port(self, type):
        return {
            'agent': 10050,
            'SNMP': 161,
            'IPMI': 623,
            'JMX': 12345
        }.get(type)

    def __repr__(self):
        return str(self.__dict__)


agent_interface = HostInterface(
    hostid=123,
    type='agent',
    main=True,
    dns='ExampleHost'
)

snmpv3_interface = HostInterface(
    hostid=123,
    type='snmp',
    main=True,
    useip=True,
    ip='10.1.1.2',
    details=dict(  # use defaults for now
        version='SNMPv3'
    )
)

print(agent_interface, snmpv3_interface)
