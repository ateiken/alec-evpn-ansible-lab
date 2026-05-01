import pynetbox
import yaml

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')

devices = nb.dcim.devices.all()
leaf_asn = nb.ipam.asns.get(description="LEAF_ASN").asn
spine_asn = nb.ipam.asns.get(description="SPINE_ASN").asn

print(f"Leaf ASN: {leaf_asn}")
print(f"Spine ASN: {spine_asn}")

for device in devices:
    print(device.name, device.device_type, device.primary_ip)

device = nb.dcim.devices.get(name='msp01-lsw01')

interfaces = nb.dcim.interfaces.filter(device_id=device.id)

for interface in interfaces:
    print(interface.name)
    ips = nb.ipam.ip_addresses.filter(interface_id=interface.id)
    for ip in ips:
        print("  ", ip.address)