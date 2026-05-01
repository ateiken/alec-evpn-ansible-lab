import pynetbox

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')

devices = nb.dcim.devices.all()

for device in devices:
    print(device.name, device.device_type, device.primary_ip)

device = nb.dcim.devices.get(name='msp01-lsw01')

interfaces = device.interfaces.all()

for interface in interfaces:
    print(interface.name, interface.mac_address, interface.mtu, interface.ipv4_addresses, interface.ipv6_addresses)
    ips = nb.ipam.ip_addresses.filter(interface_id=interface.id)
    # for ip in ips:
    #     print("  ", ip.address, ip.family)