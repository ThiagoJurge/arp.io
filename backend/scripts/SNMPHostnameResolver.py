import json
import multiprocessing
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

class SNMPHostnameResolver:
    def __init__(self, community='altarede8169', port=161, storage_file='hostnames.json'):
        self.community = community
        self.port = port
        self.storage_file = storage_file
        self.hostnames = self._load_hostnames()

    def _load_hostnames(self):
        try:
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _save_hostname(self, ip_address, hostname):
        self.hostnames[ip_address] = hostname
        with open(self.storage_file, 'w') as file:
            json.dump(self.hostnames, file, indent=4)

    def _resolve_single_ip(self, ip_address):
        if ip_address in self.hostnames:
            return self.hostnames[ip_address]

        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((ip_address, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))  # OID for sysName
            )

            error_indication, error_status, error_index, var_binds = next(iterator)

            if error_indication:
                print(f"SNMP error: {error_indication}")
                return ip_address

            for var_bind in var_binds:
                hostname = str(var_bind[1])
                self._save_hostname(ip_address, hostname)
                return hostname

        except Exception as e:
            print(f"SNMP exception: {e}")
            return ip_address

    def resolve_hostnames(self, ip_addresses):
        with multiprocessing.Pool() as pool:
            results = pool.map(self._resolve_single_ip, ip_addresses)
            return results