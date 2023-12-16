import json
from pythonping import ping
import ipaddress
from pysnmp.hlapi import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
)


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(ObjectType(ObjectIdentity(oid)))
    return object_types


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError("Got SNMP error: {0}".format(error_indication))
        except StopIteration:
            break
    return result


def get(
    target, oids, credentials, port=161, engine=SnmpEngine(), context=ContextData()
):
    handler = getCmd(
        engine,
        credentials,
        UdpTransportTarget((target, port), timeout=5.0),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def ping_and_resolve(ip, community):
    response = ping(ip, count=1, timeout=1)
    if response.success():
        hostname_snmp = get(ip, ["1.3.6.1.2.1.1.5.0"], CommunityData(community))
        hostname = hostname_snmp.get("1.3.6.1.2.1.1.5.0", None)
        return {"ip": ip, "hostname": hostname}
    else:
        pass


def main():
    community = "altarede8169"  # Substitua pela sua community string SNMP
    ip_list = [
        "10.22.0.1",
        "10.22.0.2",
        "10.22.0.3",
        "10.22.0.4",
        "10.22.0.5",
        "10.22.0.6",
        "10.22.0.8",
        "10.22.0.9",
        "10.22.0.10",
        "10.22.0.11",
        "10.22.0.12",
        "10.22.0.14",
        "10.22.0.15",
        "10.22.0.16",
        "10.22.0.17",
        "10.22.0.18",
        "10.22.0.19",
        "10.22.0.20",
        "10.22.0.21",
        "10.22.0.22",
        "10.22.0.23",
        "10.22.0.24",
        "10.22.0.25",
        "10.22.0.26",
        "10.22.0.27",
        "10.22.0.28",
        "10.22.0.29",
        "10.22.0.30",
        "10.22.0.31",
        "10.22.0.32",
        "10.22.0.33",
        "10.22.0.34",
        "10.22.0.35",
        "10.22.0.36",
        "10.22.0.37",
        "10.22.0.38",
        "10.22.0.40",
        "10.22.0.41",
        "10.22.0.42",
        "10.22.0.44",
        "10.22.0.45",
        "10.22.0.46",
        "10.22.0.47",
        "10.22.0.48",
        "10.22.0.49",
        "10.22.0.50",
        "10.22.0.51",
        "10.22.0.52",
        "10.22.0.53",
        "10.22.0.54",
        "10.22.0.55",
        "10.22.0.56",
        "10.22.0.57",
        "10.22.0.58",
        "10.22.0.62",
        "10.22.0.63",
        "10.22.0.64",
        "10.22.0.65",
        "10.22.0.66",
        "10.22.0.67",
        "10.22.0.68",
        "10.22.0.69",
        "10.22.0.70",
        "10.22.0.71",
        "10.22.0.72",
        "10.22.0.73",
        "10.22.0.74",
        "10.22.0.75",
        "10.22.0.76",
        "10.22.0.77",
        "10.22.0.78",
        "10.22.0.79",
        "10.22.0.80",
        "10.22.0.82",
        "10.22.0.84",
        "10.22.0.87",
        "10.22.0.88",
        "10.22.0.89",
        "10.22.0.83",
        "10.22.0.90",
        "10.22.0.85",
        "10.22.0.86",
        "10.22.0.91",
        "10.22.0.92",
        "10.22.0.93",
        "10.22.0.94",
        "10.22.0.95",
        "10.22.0.97",
        "10.22.0.98",
        "10.22.0.99",
        "10.22.0.100",
        "10.22.0.101",
        "10.22.0.102",
        "10.22.0.103",
        "10.22.0.104",
        "10.22.0.105",
        "10.22.0.106",
        "10.22.0.107",
        "10.22.0.108",
        "10.22.0.109",
        "10.22.0.110",
        "10.22.0.111",
        "10.22.0.112",
        "10.22.0.114",
        "10.22.0.115",
        "10.22.0.117",
        "10.22.0.118",
        "10.22.0.119",
        "10.22.0.120",
        "10.22.0.121",
        "10.22.0.122",
        "10.22.0.123",
        "10.22.0.124",
        "10.22.0.125",
        "10.22.0.127",
        "10.22.0.128",
        "10.22.0.129",
        "10.22.0.130",
        "10.22.0.131",
        "10.22.0.132",
        "10.22.0.134",
        "10.22.0.135",
        # "10.22.0.137",
        "10.22.0.139",
        "10.22.0.140",
        # "10.22.0.141",
        # "10.22.0.142",
        "10.22.0.143",
        "10.22.0.144",
        "10.22.0.145",
        # "10.22.0.146",
        "10.22.0.147",
        "10.22.0.148",
        "10.22.0.149",
        "10.22.0.151",
        "10.22.0.152",
        # "10.22.0.153",
        "10.22.0.200",
        "10.22.0.201",
        "10.22.0.254",
        "10.22.1.0",
    ]
    results = []
    for ip in ip_list:
        result = ping_and_resolve(str(ip), community)
        results.append(result)

    with open("hostnames.json", "w") as outfile:
        json.dump(results, outfile, indent=4)


if __name__ == "__main__":
    main()
