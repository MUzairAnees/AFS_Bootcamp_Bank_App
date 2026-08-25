from abc import ABC, abstractmethod
from decimal import Decimal
from bankapp.exceptions import InsufficientFundsError, BankError


class Account(ABC):
    '''
    Account(ABC):
    It serves as a base class for the account classes: SavingsAccount() and CheckingAccount().
    This class is never going to be called directly; Only through child classes.

    Shared attributes: account_number, owner_id and balance.

    balance(self): is a getter for the account balance. Made into a @property so we can read the amount but not write to it.

    deposit(self, amount): deposits an amount into the account as long as it's not negative.

    withdraw(self, amount): @abstractmethod applied so that each child can define its own withdrawal rules.
    '''

    def __init__(self, account_number: int, owner_id: int, balance: Decimal = Decimal("0")):
        self.account_number = account_number
        self.owner_id = owner_id
        self._balance = balance

    @property
    def balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("Trying to deposit a negative amount to a bank account.")
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount: Decimal):
        pass

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{classname}({self.account_number}, {self.owner_id}, {self.balance})"

class SavingsAccount(Account):
    '''
    SavingsAccount(Account):
    SavingsAccount extends the base Account class.
    This allows for SavingsAccount to receive base attributes (account_number, owner_id and balance).
    It doesn't have its own specific attributes.
    Allows withdrawal as long as the amount is not negative and amount is not more than balance.
    '''
    def withdraw(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("Trying to withdraw a negative amount to a bank account.")

        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds in your savings account.")
        self._balance -= amount

class CheckingAccount(Account):
    '''
    CheckingAccount(Account):
    CheckingAccount extends the base Account class.
    This allows for CheckingAccount to receive base attributes (account_number, owner_id and balance).
    It doesn't have its own specific attributes.
    Allows withdrawal as long as the amount is not negative and balance after withdrawal would be more than -500 dollars.
    '''
    OVERDRAFT_LIMIT = Decimal("500")

    def withdraw(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("Trying to withdraw a negative amount to a bank account.")

        new_balance = self._balance - amount
        if new_balance < -self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError("Insufficient funds. You are overdrawn by more than 500 dollars.")
        self._balance -= amount