#не менее 6 символ 1 цифра 
def check(s):
    cnt = 0
    if len(s) >= 6:
        for ch in s:
            if ch in "0123456789":
                cnt+=1
        if cnt >= 1:
            return True
        elif cnt ==0: 
            return False
        return True
    else: return False

    return False

s = input("Enter: ")
print(check(s))