thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

thislist.insert(1, "melon")
print(thislist)

thistuple = ("kiwi", "pear")
thislist.extend(thistuple)
print(thislist) 

thislist.remove("banana")
print(thislist)