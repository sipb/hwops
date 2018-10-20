import yaml
import db

with open("input.yaml", "r") as f:
    servers = yaml.safe_load(f)["servers"]

devices = []
for server in servers:
    if type(server["slot"]) == int:
        start = end = server["slot"]
    else:
        rr = server["slot"].split("-")
        start, end = map(int, rr)
    devices.append(db.Devices(rack=server["rack"], rack_first_slot=start, rack_last_slot=end, name=server.get("hostname", server.get("name", "")), comments=server.get("comment", ""), model=server.get("type", ""), ip="", contact="unknown", service_level="unknown", last_updated_by="cela"))

db.session.add_all(devices)
db.session.commit()
