import copy
import random
from decimal import Decimal
from bankapp.user import Customer
from bankapp.exceptions import NotFoundError
from bankapp.transaction import Transaction, TransactionType
from bankapp.seed import USERS, ACCOUNTS, BRANCHES

class Bank:
    '''
    Bank():
    Directly accessible class.
    Bank object holds all the user objects in a list, all the accounts in a list,
    all the transaction records in a list, and all the branches in a list
    [change collection method after].
    '''
    def __init__(self):
        self.users = []
        self.accounts = []
        self.transactions = []
        self.branches = []


#-------------------------user--------------------------#
    def add_user(self, user):
        '''
        adds a new user to users list of bank object.
        '''
        self.users.append(user)

    def username_exists(self, username):
        '''
        Checks whether any user (Admin or Customer) already has this username.
        Checked against all users, not just customers, since Bank.login()
        matches against everyone regardless of type.
        '''
        return any(user.username == username for user in self.users)

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

    def _generate_account_number(self):
        '''
        Generates a unique 4-digit account number.
        Picks a random int and regenerates on collision against account_numbers
        already present in self.accounts, so uniqueness is guaranteed rather
        than merely likely.
        '''
        existing_numbers = {account.account_number for account in self.accounts}
        while True:
            candidate = random.randint(1000, 9999)
            if candidate not in existing_numbers:
                return candidate


#------------------------branch------------------------#
    def add_branch(self, branch):
        '''
        adds a new branch to branches list of bank object.
        Used for seeding -> branches are fixed at 5 and never created at runtime.
        '''
        self.branches.append(branch)

    def find_branch(self, branch_code):
        '''
        finds a branch by looping through bank obj branches list and comparing with passed param.
        Raises NotFoundError if no branch has that code -> lets callers validate
        admin-entered branch codes with the same try/except pattern used for
        find_customer/find_account.
        '''
        for branch in self.branches:
            if branch.branch_code == branch_code:
                return branch

        raise NotFoundError("Branch not found")

    def get_branch_customers(self, branch):
        '''
        Returns every Customer whose branch_id matches the given branch's
        branch_code. Each returned Customer already carries its own .accounts
        list, so this answers "which accounts belong to this branch" too,
        without needing to separately collect Account objects.
        '''
        return [
            user for user in self.users
            if isinstance(user, Customer) and user.branch_id == branch.branch_code
        ]

    def get_branch_transaction_volume(self, branch):
        '''
        Returns the total transaction volume (sum of Transaction.amount) for
        every transaction touching an account owned by a customer at the given
        branch. All-time total -> month/date filtering is deferred to a future
        refactor, not implemented here.
        '''
        branch_customers = self.get_branch_customers(branch)
        account_numbers = {
            account.account_number
            for customer in branch_customers
            for account in customer.accounts
        }
        matching_transactions = [
            transaction for transaction in self.transactions
            if transaction.from_account in account_numbers or transaction.to_account in account_numbers
        ]
        return sum((transaction.amount for transaction in matching_transactions), Decimal("0"))

    def get_branches_over_staff_ratio(self, limit):
        '''
        Returns every Branch whose staff-to-manager ratio exceeds the given
        limit. Every branch has exactly one manager, so the ratio is just
        branch.staff itself.
        '''
        return [branch for branch in self.branches if branch.staff > limit]


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

    def get_transactions(self, customer=None):
        '''
        Returns transactions newest first. With no customer given, returns
        every transaction the bank has recorded (the admin view). With a
        customer given, filters to only transactions where from_account or
        to_account matches one of that customer's account_numbers.
        '''
        if customer is None:
            matches = self.transactions
        else:
            account_numbers = {account.account_number for account in customer.accounts}
            matches = [
                transaction for transaction in self.transactions
                if transaction.from_account in account_numbers or transaction.to_account in account_numbers
            ]

        return list(reversed(matches))

#-----------------------operations-----------------------#
    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None


#------------------------seed data-----------------------#
def create_bank():
    '''
    Builds a fresh Bank from the seed data.
    Seed lists are deep-copied so every call produces independent objects ->
    mutating a customer/account/branch in one Bank can never leak into a
    Bank built by a later call in the same process.
    '''
    bank = Bank()

    for user in copy.deepcopy(USERS):
        bank.add_user(user)

    for account in copy.deepcopy(ACCOUNTS):
        bank.add_account(account)

    for branch in copy.deepcopy(BRANCHES):
        bank.add_branch(branch)

    return bank