class Account:
    def __init__(self,owner,balance=0.0):
        self.owner= owner
        self.balance= balance
    def deposit(self,amount):
        if amount>0:
            self.balance+=amount
            print(f"Deposit of ${amount:.2f} successful. New balance: ${self.balance:.2f}")
        else: print("Deposit amount must be positive.")

    def withdraw(self,amount):
        if amount > self.balance:
            print("Insufficient funds. Withdrawal denied.")
        elif amount > 0:
            self.balance-=amount
            print(f"Withdrawal of ${amount:.2f} successful. New balance: ${self.balance:.2f}")
        else: print("Withdrawal amount must be positive.")

    def show_balance(self):
        print(f"Account owner: {self.owner}, Balance: ${self.balance:.2f}")

owner_name = input("Enter account owner's name: ")
initial_balance = float(input("Enter initial balance: "))

account = Account(owner_name, initial_balance)

account.show_balance()
deposit_amount = float(input("Enter deposit amount: "))
account.deposit(deposit_amount)

withdraw_amount = float(input("Enter withdrawal amount: "))
account.withdraw(withdraw_amount)

account.show_balance()
