class Account():
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def print_balance(self):
        print(self.balance)

    def print_owner(self):
        print(self.owner)

    def deposit(self, money):
        self.balance += money
        print("Deposit accepted.")

    def withdrawal(self, money):
        if self.balance >= money:
            self.balance -= money
            print("Withdrawal accepted.")
        else:
            print("Unavailable.")


acc1 = Account(input(), int(input()))
acc1.deposit(int(input()))
acc1.withdrawal(int(input()))
acc1.print_balance()
acc1.print_owner()
