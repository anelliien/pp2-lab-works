import json

with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 78)
print(f"{'DN':<51}{'Description':<20}{'Speed':<10}{'MTU':<6}")
print(f"{('-'*50) :<51}{('-'*18):<20}{('-'*6):<9}{('-'*6):<6}")

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    description = attributes.get("descr","") 
    speed = attributes["speed"]
    mtu = attributes["mtu"]
    print(f"{dn:<51}{description:<19}{speed:<11}{mtu:<6}")
