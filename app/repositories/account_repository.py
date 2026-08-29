import random
from abc import ABC, abstractmethod
from decimal import Decimal

from app.exceptions import NotFoundError
from app.models.account import Account


class AccountRepository(ABC):
    '''
    AccountRepository(ABC):
    Contract for account storage. Any implementation - in-memory now,
    MongoDB in Phase 12 - must provide every method below.

    Same active/inactive asymmetry as CustomerRepository: list_all()
    hides deactivated accounts by default, find_by_number() always
    returns them so closed accounts stay readable and the transactions
    referencing them stay resolvable.

    owner_ids is plural because accounts carry no branch_id. Filtering
    accounts by branch resolves through customers first, producing a set
    of owner ids -> a singular owner_id could not express that query, and
    the caller would have to load every account and filter in Python.

    min_balance uses >= (an account holding exactly the limit is included),
    unlike BranchRepository's staff_over, which is strict.
    '''

    @abstractmethod
    def add(self, account: Account) -> None:
        pass

    @abstractmethod
    def save(self, account: Account) -> None:
        pass

    @abstractmethod
    def find_by_number(self, account_number: int) -> Account:
        pass

    @abstractmethod
    def list_all(self, owner_ids: list[int] | None = None,
                 min_balance: Decimal | None = None,
                 include_inactive: bool = False) -> list[Account]:
        pass

    @abstractmethod
    def generate_account_number(self) -> int:
        pass


class InMemoryAccountRepository(AccountRepository):
    '''
    Stores accounts in a dict keyed by account_number.
    '''

    def __init__(self):
        self._accounts: dict[int, Account] = {}

    def add(self, account: Account) -> None:
        self._accounts[account.account_number] = account

    def save(self, account: Account) -> None:
        self._accounts[account.account_number] = account

    def find_by_number(self, account_number: int) -> Account:
        account = self._accounts.get(account_number)
        if account is None:
            raise NotFoundError("Account not found")
        return account

    def list_all(self, owner_ids: list[int] | None = None,
                 min_balance: Decimal | None = None,
                 include_inactive: bool = False) -> list[Account]:
        accounts = list(self._accounts.values())
        if not include_inactive:
            accounts = [a for a in accounts if a.is_active]
        if owner_ids is not None:
            owner_set = set(owner_ids)
            accounts = [a for a in accounts if a.owner_id in owner_set]
        if min_balance is not None:
            accounts = [a for a in accounts if a.balance >= min_balance]
        return accounts

    def generate_account_number(self) -> int:
        while True:
            candidate = random.randint(1000, 9999)
            if candidate not in self._accounts:
                return candidate
