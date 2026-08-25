from decimal import Decimal
from bankapp.account import SavingsAccount, CheckingAccount
from bankapp.user import Customer, USERS
from bankapp.exceptions import NotFoundError

class Bank:
    '''
    Bank():
    Directly accessible class.
    Bank object holds all the user objects in a list, and all the accounts in a list [change collection method after].
    '''
    def __init__(self):
        self.users = []
        self.accounts = []


#-------------------------user--------------------------#
    def add_user(self, user):
        '''
        adds a new user to users list of bank object.
        '''
        self.users.append(user)

    def find_customer(self, customer_id):
        '''
        finds a customer user by looping through bank obj users list and comparing with passed param.
        '''
        for user in self.users:
            if isinstance(user, Customer):
                if user.customer_id == customer_id:
                    return user

        raise NotFoundError("Customer not found")

    def remove_customer(self, customer_id):
        '''
        removes a customer by bank obj calling find_customer and
        '''
        customer_to_remove = self.find_customer(customer_id)

        for acc in list(customer_to_remove.accounts):
            self.accounts.remove(acc)

        self.users.remove(customer_to_remove)


#------------------------account------------------------#
    def add_account(self, account):
        owner = self.find_customer(account.owner_id)
        self.accounts.append(account)
        owner.accounts.append(account)

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account

        raise NotFoundError("Account not found")


#-----------------------operations-----------------------#
    def transfer(self, from_account, to_account, amount):
        from_account.withdraw(amount)
        to_account.deposit(amount)

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None


#------------------------seed data-----------------------#
def create_bank():
    bank = Bank()

    for user in USERS:
        bank.add_user(user)

    bank.add_account(SavingsAccount(1001, 97, Decimal("1000")))
    bank.add_account(SavingsAccount(1002, 98, Decimal("99000")))
    bank.add_account(SavingsAccount(1003, 99, Decimal("59000")))
    bank.add_account(CheckingAccount(2001, 97, Decimal("900")))

    return bank