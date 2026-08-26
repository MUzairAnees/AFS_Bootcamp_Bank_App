import random
from decimal import Decimal
from bankapp.account import SavingsAccount, CheckingAccount
from bankapp.user import Customer, USERS
from bankapp.exceptions import NotFoundError
from bankapp.transaction import Transaction, TransactionType

class Bank:
    '''
    Bank():
    Directly accessible class.
    Bank object holds all the user objects in a list, all the accounts in a list,
    and all the transaction records in a list [change collection method after].
    '''
    def __init__(self):
        self.users = []
        self.accounts = []
        self.transactions = []


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


#----------------------transactions-----------------------#
    def _generate_transaction_id(self):
        '''
        Generates a unique 10-digit transaction id.
        Picks a random int and regenerates on collision against ids
        already present in self.transactions, so uniqueness is guaranteed
        rather than merely likely.
        '''
        existing_ids = {transaction.transaction_id for transaction in self.transactions}
        while True:
            candidate = random.randint(1_000_000_000, 9_999_999_999)
            if candidate not in existing_ids:
                return candidate

    def deposit(self, account, amount):
        '''
        Deposits amount into account, then records the deposit as a
        Transaction. account.deposit() runs first so a failed deposit
        (e.g. negative amount, raises ValueError) never produces a
        Transaction record.
        '''
        account.deposit(amount)
        transaction = Transaction(
            transaction_id=self._generate_transaction_id(),
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            to_account=account.account_number
        )
        self.transactions.append(transaction)

    def withdraw(self, account, amount):
        '''
        Withdraws amount from account, then records the withdrawal as a
        Transaction. account.withdraw() runs first so a failed withdrawal
        (e.g. negative amount or insufficient funds, raises ValueError or
        InsufficientFundsError) never produces a Transaction record.
        '''
        account.withdraw(amount)
        transaction = Transaction(
            transaction_id=self._generate_transaction_id(),
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount,
            from_account=account.account_number
        )
        self.transactions.append(transaction)

    def transfer(self, from_account, to_account, amount):
        '''
        Withdraws amount from from_account and deposits it into to_account,
        then records the transfer as a Transaction. Both account operations
        run first so a failed transfer (e.g. insufficient funds on the
        withdrawal) never produces a Transaction record.
        '''
        from_account.withdraw(amount)
        to_account.deposit(amount)
        transaction = Transaction(
            transaction_id=self._generate_transaction_id(),
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
            from_account=from_account.account_number,
            to_account=to_account.account_number
        )
        self.transactions.append(transaction)

#-----------------------operations-----------------------#
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