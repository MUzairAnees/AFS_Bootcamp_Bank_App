from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.exceptions import InsufficientFundsError
from app.models.account import CheckingAccount, SavingsAccount
from app.models.branch import Branch
from app.models.transaction import Transaction, TransactionType
from app.models.user import Admin, Customer


# ---------- Account: shared behaviour ----------

def test_account_defaults_to_zero_balance_and_active():
    account = SavingsAccount(1001, 97)
    assert account.balance == Decimal("0")
    assert account.is_active is True


def test_deposit_of_zero_is_rejected():
    account = SavingsAccount(1001, 97, Decimal("100"))
    with pytest.raises(ValueError):
        account.deposit(Decimal("0"))


def test_deposit_of_negative_is_rejected():
    account = SavingsAccount(1001, 97, Decimal("100"))
    with pytest.raises(ValueError):
        account.deposit(Decimal("-5"))


def test_balance_cannot_be_assigned_directly():
    account = SavingsAccount(1001, 97, Decimal("100"))
    with pytest.raises(AttributeError):
        account.balance = Decimal("999999")


# ---------- SavingsAccount: no overdraft ----------

def test_savings_can_withdraw_exact_balance():
    account = SavingsAccount(1001, 97, Decimal("1000"))
    account.withdraw(Decimal("1000"))
    assert account.balance == Decimal("0")


def test_savings_rejects_one_cent_over_balance():
    account = SavingsAccount(1001, 97, Decimal("1000"))
    with pytest.raises(InsufficientFundsError):
        account.withdraw(Decimal("1000.01"))


# ---------- CheckingAccount: overdraft boundary ----------

def test_checking_allows_withdrawal_to_exactly_the_overdraft_limit():
    account = CheckingAccount(2001, 97, Decimal("900"))
    account.withdraw(Decimal("1400"))
    assert account.balance == Decimal("-500")


def test_checking_rejects_one_cent_past_the_overdraft_limit():
    account = CheckingAccount(2001, 97, Decimal("900"))
    with pytest.raises(InsufficientFundsError):
        account.withdraw(Decimal("1400.01"))


def test_checking_allows_withdrawal_just_inside_the_limit():
    account = CheckingAccount(2001, 97, Decimal("900"))
    account.withdraw(Decimal("1399.99"))
    assert account.balance == Decimal("-499.99")


# ---------- Customer ----------

def test_customer_defaults_to_active():
    customer = Customer(97, "Uzair", "u@x.com", 1, "Uzair1", "pw")
    assert customer.is_active is True


def test_customer_does_not_hold_accounts():
    customer = Customer(97, "Uzair", "u@x.com", 1, "Uzair1", "pw")
    assert not hasattr(customer, "accounts")


def test_admin_has_no_is_active_flag():
    admin = Admin(1001, "admin1", "pw")
    assert not hasattr(admin, "is_active")


# ---------- Transaction ----------

def test_transaction_timestamp_is_timezone_aware_utc():
    transaction = Transaction(1, TransactionType.DEPOSIT, Decimal("100"), to_account=1001)
    assert transaction.timestamp.tzinfo is not None
    assert transaction.timestamp.utcoffset() == timezone.utc.utcoffset(None)


def test_transaction_accepts_an_explicit_timestamp():
    stamp = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    transaction = Transaction(1, TransactionType.DEPOSIT, Decimal("100"),
                              to_account=1001, timestamp=stamp)
    assert transaction.timestamp == stamp


def test_transaction_has_no_is_active_flag():
    transaction = Transaction(1, TransactionType.DEPOSIT, Decimal("100"), to_account=1001)
    assert not hasattr(transaction, "is_active")


def test_deposit_has_no_from_account():
    transaction = Transaction(1, TransactionType.DEPOSIT, Decimal("100"), to_account=1001)
    assert transaction.from_account is None
    assert transaction.to_account == 1001


# ---------- Branch ----------

def test_branch_defaults_to_zero_staff():
    branch = Branch(1, "Austin", 1001)
    assert branch.staff == 0


def test_branch_has_no_is_active_flag():
    branch = Branch(1, "Austin", 1001, 6)
    assert not hasattr(branch, "is_active")
