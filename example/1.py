class Account:
    def __init__(self, owner, balance =0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Снятие из депозита прошла успешно. Баланс: {self.balance:.2f}")
    def withdraw(self, amount):
        if amount > self.balance:
            print("Сумма превышает баланс!")
        else:
            self.balance-=amount
            print(f"Снятие успешно прошло. Баланс: {self.balance:.2f}")
    def show(self):
        print(f"Имя владельца: {self.owner}, Баланс: {self.balance:.2f}")

owners_name = input("Введите имя владельца: ")
balance = float(input("Введите исходный баланс: "))
account = Account(owners_name, balance)
account.show()

dep_amount = float(input())
account.deposit(dep_amount)

witht_amount = float(input())
account.withdraw(witht_amount)

account.show()