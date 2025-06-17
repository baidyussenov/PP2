import json

with open(r"C:\Users\Sattigali\Desktop\PP2\lab 4\Json\sample-data.json") as f:
    data= json.load(f)

print("Interfae Status")
print("=" * 80)
print(f"{'DN':<50}{'Description':<20}{'Speed':<10}{'MTU':<5}")
print("-" * 80)

for item in data["imdata"][:3]:
    attrs = item["l1PhysIf"]["attributes"]
    dn = attrs["dn"]
    descrip = attrs.get("descr", "")
    speed = attrs.get("speed", "inherit")
    mtu = attrs["mtu"]
    print(f"{dn:<50}{descrip:<20}{speed:<10}{mtu:<5}")