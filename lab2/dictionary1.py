thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)

print(thisdict["brand"])

x = thisdict.items()

print(x) #before the change

thisdict["color"] = "red"

print(x) #after the change