def has_33(thislist):
    for i in range(len(thislist)-1):
        if thislist[i] == '3' and thislist[i+1] == '3':
            return True
    return False

thislist=input().split()
if has_33(thislist):
    print(True)
else: print(False)