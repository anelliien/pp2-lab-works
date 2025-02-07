def has_007(thislist):
    for i in range(len(thislist)-2):
        if thislist[i] == '0' and thislist[i+1] == '0' and thislist[i+2] == '7':
            return True
    return False

thislist=input().split()
if has_007(thislist):
    print(True)
else: print(False)