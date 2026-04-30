import pynetbox

nb = pynetbox.api('http://192.168.8.10:8080', token='j7NLkeIibHoVz60Tfs6rHn0bp4FjVg2mkfXQBRqJ')

devices = nb.dcim.devices.all()

for device in devices:
    print(device.name, device.device_role.slug)