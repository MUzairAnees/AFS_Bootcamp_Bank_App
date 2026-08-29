import random
from abc import ABC, abstractmethod
from datetime import datetime

from app.exceptions import NotFoundError
from app.models.transaction import Transaction, TransactionType


class TransactionRepository(ABC):
    '''
    TransactionRepository(ABC):
    Contract for transaction storage. Any implementation - in-memory now,
    MongoDB in Phase 12 - must provide every method below.

    There is no save() and no include_inactive: transactions are immutable
    financial records. Once written they are never edited, deactivated or
    removed, even when the accounts they reference are deactivated.

    account_numbers is plural for the same reason AccountRepository takes
    owner_ids -> filtering by customer or by branch resolves to a set of
    accounts, and a singular parameter could not express that query.

    Results come back newest first, sorted on timestamp rather than
    insertion order, since a Transaction may be constructed with an
    explicit timestamp.

    start_date/end_date are plain datetime bounds compared with >= and <=.
    Turning a date string like "2026-01-01" into the right UTC boundary is
    the API layer's job, so the convention lives in one place and this stays
    a simple range filter.
    '''

    @abstractmethod
    def add(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def find_by_id(self, transaction_id: int) -> Transaction:
        pass

    @abstractmethod
    def list_all(self, account_numbers: list[int] | None = None,
                 start_date: datetime | None = None,
                 end_date: datetime | None = None,
                 transaction_type: TransactionType | None = None) -> list[Transaction]:
        pass

    @abstractmethod
    def generate_transaction_id(self) -> int:
        pass


class InMemoryTransactionRepository(TransactionRepository):
    '''
    Stores transactions in a dict keyed by transaction_id.
    '''

    def __init__(self):
        self._transactions: dict[int, Transaction] = {}

    def add(self, transaction: Transaction) -> None:
        self._transactions[transaction.transaction_id] = transaction

    def find_by_id(self, transaction_id: int) -> Transaction:
        transaction = self._transactions.get(transaction_id)
        if transaction is None:
            raise NotFoundError("Transaction not found")
        return transaction

    def list_all(self, account_numbers: list[int] | None = None,
                 start_date: datetime | None = None,
                 end_date: datetime | None = None,
                 transaction_type: TransactionType | None = None) -> list[Transaction]:
        transactions = list(self._transactions.values())

        if account_numbers is not None:
            wanted = set(account_numbers)
            transactions = [t for t in transactions
                            if t.from_account in wanted or t.to_account in wanted]
        if start_date is not None:
            transactions = [t for t in transactions if t.timestamp >= start_date]
        if end_date is not None:
            transactions = [t for t in transactions if t.timestamp <= end_date]
        if transaction_type is not None:
            transactions = [t for t in transactions if t.type is transaction_type]

        return sorted(transactions, key=lambda t: t.timestamp, reverse=True)

    def generate_transaction_id(self) -> int:
        while True:
            candidate = random.randint(1_000_000_000, 9_999_999_999)
            if candidate not in self._transactions:
                return candidate
