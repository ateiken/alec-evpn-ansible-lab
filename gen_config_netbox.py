import pynetbox
import yaml
import ipaddress
from pprint import pprint

nb = pynetbox.api('http://192.168.8.10:8080', token='wu4VAC2xlNwk2aAtSzF2KFODDrFVSSzaOf0mUveG')


# get ASNs from NetBox
leaf_asn = nb.ipam.asns.get(description="LEAF_ASN").asn
spine_asn = nb.ipam.asns.get(description="SPINE_ASN").asn

print(f"Leaf ASN: {leaf_asn}")
print(f"Spine ASN: {spine_asn}")

# get all devices
devices = nb.dcim.devices.all()
# for device in devices:
#     print(device.name, device.role.slug)
#     interfaces = nb.dcim.interfaces.filter(device_id=device.id)
#     for interface in interfaces:
#         ips = list(nb.ipam.ip_addresses.filter(interface_id=interface.id))
#         if ips:  # only print interfaces that have IPs
#             print(f"  {interface.name}: {ips[0].address}")

for device in devices:
    d = {}
    d['hostname'] = device.name
    d['interfaces'] = []
    d['bgp_neighbors'] = []

    if device.role.slug == 'leaf-switch':
        d['asn'] = leaf_asn
        remote_asn = spine_asn
    elif device.role.slug == 'spine-switch':
        d['asn'] = spine_asn
        remote_asn = leaf_asn

    interfaces = nb.dcim.interfaces.filter(device_id=device.id)
    for interface in interfaces:
        ips = list(nb.ipam.ip_addresses.filter(interface_id=interface.id))
        if ips:  # only include interfaces that have IPs
            ip = ips[0].address
            ip_only = ip.split('/')[0]  # remove subnet mask
            mask_only = ip.split('/')[1]  # get subnet mask
            if interface.name == 'lo0':
                d['loopback0_ip'] = ip_only
            elif interface.name == 'lo1':
                d['loopback1_ip'] = ip_only
            elif interface.name == 'mgmt':
                d['ansible_host'] = ip_only
            elif 'ethernet' in interface.name.lower():
                d['interfaces'].append({
                    'interface': interface.name,
                    'ip': ip_only, 
                    'mask': '/' + mask_only
                })
                network = ipaddress.ip_interface(ip).network
                hosts = list(network.hosts())
                neighbor_ip = str(hosts[0]) if ip_only == str(hosts[1]) else str(hosts[1])
                d['bgp_neighbors'].append({
                    'neighbor': neighbor_ip,
                    'remote_as': remote_asn,
                    'state': 'present'
                })
    pprint(d)
    print()