class Mentors:
    def __init__(self, s):
        self.s=s
    def Mentor1(self, amount = 0):
        for i in self.s:
            str(i)
            if i in '0123456789':
                amount +=1
        print(f"Число цифр в строке: {amount}")
    def Mentor2(self, amount2 = 0):
        for x in self.s:
            str(x)
            if (x >= "A" and x <= "Z") or (x >= "a" and x <= "z"):
                amount2 +=1
        print(f"Число букв в строке: {amount2}")

s = str(input("Введите строку "))
st = Mentors(s)
st.Mentor1()
st.Mentor2()
            
