from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum


class TransactionType(Enum):
    '''
    TransactionType(Enum):
    Enumerates the kinds of transactions the bank can record.
    Used instead of raw strings so a typo (e.g. "Depost") fails immediately
    instead of silently breaking reporting/filtering logic later.
    '''
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    TRANSFER = "Transfer"


class Transaction:
    '''
    Transaction():
    Represents a single record of money moving through the bank.
    Not tied to live Account objects -> stores account_numbers (int)
    instead of Account references, matching the ID-based linking style
    already used elsewhere (Account.owner_id, Customer.branch_id).

    Has no is_active flag -> transactions are immutable financial records.
    They are never edited or deactivated, even when the accounts they
    reference are.

    Attributes:
    transaction_id: unique identifier for this transaction. Generated and
    assigned by whatever creates the Transaction (e.g. the repository) - not
    generated internally, same as how Account/Customer ids are handed in.

    type: a TransactionType value (DEPOSIT / WITHDRAWAL / TRANSFER).

    amount: Decimal amount moved. Always stored positive; direction is
    expressed via from_account/to_account, not by sign.

    from_account: account_number (int) the money left, or None if this
    transaction has no originating account (e.g. a plain deposit).

    to_account: account_number (int) the money landed in, or None if this
    transaction has no destination account (e.g. a plain withdrawal).

    timestamp: timezone-aware datetime in UTC, defaulting to "now" at
    construction time. Stored in UTC so timestamps stay comparable and
    unambiguous regardless of where the server runs.
    '''

    def __init__(self, transaction_id: int, transaction_type: TransactionType, amount: Decimal,
                 from_account: int | None = None, to_account: int | None = None,
                 timestamp: datetime | None = None):
        self.transaction_id = transaction_id
        self.type = transaction_type
        self.amount = amount
        self.from_account = from_account
        self.to_account = to_account
        self.timestamp = timestamp if timestamp is not None else datetime.now(timezone.utc)

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return (f"{classname}({self.transaction_id}, {self.type.value}, {self.amount}, "
                f"from={self.from_account}, to={self.to_account}, at={self.timestamp})")
