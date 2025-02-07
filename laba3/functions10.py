def Unique(thislist):
    unique_list = []
    for x in thislist:
       if x not in unique_list:
           unique_list.append(x)
    print(unique_list)
    

thislist= input().split()
Unique(thislist)