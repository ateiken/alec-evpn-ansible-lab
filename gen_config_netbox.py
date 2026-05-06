import pynetbox
import yaml

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')


# get ASNs from NetBox
leaf_asn = nb.ipam.asns.get(description="LEAF_ASN").asn
spine_asn = nb.ipam.asns.get(description="SPINE_ASN").asn

print(f"Leaf ASN: {leaf_asn}")
print(f"Spine ASN: {spine_asn}")

# get all devices
devices = nb.dcim.devices.all()
for device in devices:
    print(device.name, device.role.slug)
    interfaces = nb.dcim.interfaces.filter(device_id=device.id)
    for interface in interfaces:
        ips = nb.ipam.ip_addresses.filter(interface_id=interface.id)
        print(f"  - {interface.name} - {ips[0].address if ips else 'No IP'}")