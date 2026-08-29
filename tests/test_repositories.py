from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.exceptions import NotFoundError
from app.models.transaction import Transaction, TransactionType
from app.repositories.branch_repository import BranchRepository


def at(day: int) -> datetime:
    return datetime(2026, 1, day, 12, 0, 0, tzinfo=timezone.utc)


# ---------- BranchRepository ----------

def test_branch_repo_lists_all_seeded_branches(branch_repo):
    assert len(branch_repo.list_all()) == 5


def test_staff_over_excludes_a_branch_at_exactly_the_limit(branch_repo):
    codes = {b.branch_code for b in branch_repo.list_all(staff_over=6)}
    assert 1 not in codes          # Austin has exactly 6
    assert codes == {2, 4}         # Houston 9, Tampa 11


def test_staff_over_zero_returns_every_branch(branch_repo):
    assert len(branch_repo.list_all(staff_over=0)) == 5


def test_find_branch_by_code(branch_repo):
    assert branch_repo.find_by_code(1).location == "Austin"


def test_find_unknown_branch_raises(branch_repo):
    with pytest.raises(NotFoundError):
        branch_repo.find_by_code(99)


# ---------- CustomerRepository ----------

def test_customer_repo_lists_active_customers_by_default(customer_repo):
    assert {c.customer_id for c in customer_repo.list_all()} == {97, 98, 99}


def test_customer_list_filters_by_branch(customer_repo):
    assert {c.customer_id for c in customer_repo.list_all(branch_id=2)} == {98}


def test_deactivated_customer_is_hidden_from_listings(customer_repo):
    tom = customer_repo.find_by_id(98)
    tom.is_active = False
    customer_repo.save(tom)
    assert 98 not in {c.customer_id for c in customer_repo.list_all()}


def test_include_inactive_shows_deactivated_customers(customer_repo):
    tom = customer_repo.find_by_id(98)
    tom.is_active = False
    customer_repo.save(tom)
    assert 98 in {c.customer_id for c in customer_repo.list_all(include_inactive=True)}


def test_find_by_id_returns_a_deactivated_customer(customer_repo):
    tom = customer_repo.find_by_id(98)
    tom.is_active = False
    customer_repo.save(tom)
    assert customer_repo.find_by_id(98).is_active is False


def test_find_unknown_customer_raises(customer_repo):
    with pytest.raises(NotFoundError):
        customer_repo.find_by_id(500)


def test_deactivated_customer_id_stays_claimed(customer_repo):
    tom = customer_repo.find_by_id(98)
    tom.is_active = False
    customer_repo.save(tom)
    assert customer_repo.exists(98) is True


def test_deactivated_username_stays_claimed(customer_repo):
    tom = customer_repo.find_by_id(98)
    tom.is_active = False
    customer_repo.save(tom)
    assert customer_repo.username_exists("TomCruise") is True


def test_username_exists_is_false_for_an_unused_name(customer_repo):
    assert customer_repo.username_exists("nobody_has_this") is False


def test_save_persists_a_change(customer_repo):
    customer = customer_repo.find_by_id(97)
    customer.name = "Renamed"
    customer_repo.save(customer)
    assert customer_repo.find_by_id(97).name == "Renamed"


# ---------- AccountRepository ----------

def test_account_repo_lists_active_accounts_by_default(account_repo):
    assert {a.account_number for a in account_repo.list_all()} == {1001, 1002, 1003, 2001}


def test_filter_accounts_by_a_single_owner(account_repo):
    numbers = {a.account_number for a in account_repo.list_all(owner_ids=[97])}
    assert numbers == {1001, 2001}


def test_filter_accounts_by_multiple_owners(account_repo):
    numbers = {a.account_number for a in account_repo.list_all(owner_ids=[97, 98])}
    assert numbers == {1001, 2001, 1002}


def test_min_balance_includes_an_account_at_exactly_the_limit(account_repo):
    numbers = {a.account_number for a in account_repo.list_all(min_balance=Decimal("900"))}
    assert 2001 in numbers          # balance is exactly 900


def test_min_balance_excludes_accounts_below_it(account_repo):
    numbers = {a.account_number for a in account_repo.list_all(min_balance=Decimal("1000"))}
    assert 2001 not in numbers      # 900 < 1000


def test_deactivated_account_is_hidden_but_still_findable(account_repo):
    account = account_repo.find_by_number(2001)
    account.is_active = False
    account_repo.save(account)
    assert 2001 not in {a.account_number for a in account_repo.list_all()}
    assert account_repo.find_by_number(2001).is_active is False


def test_find_unknown_account_raises(account_repo):
    with pytest.raises(NotFoundError):
        account_repo.find_by_number(9999)


def test_generated_account_numbers_are_four_digits(account_repo):
    for _ in range(50):
        number = account_repo.generate_account_number()
        assert 1000 <= number <= 9999


def test_generated_account_numbers_never_collide_with_stored_ones(account_repo):
    stored = {1001, 1002, 1003, 2001}
    for _ in range(200):
        assert account_repo.generate_account_number() not in stored


# ---------- TransactionRepository ----------

def test_transaction_repo_starts_empty(transaction_repo):
    assert transaction_repo.list_all() == []


def test_add_and_find_a_transaction(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.DEPOSIT, Decimal("100"), to_account=1001))
    assert transaction_repo.find_by_id(1).amount == Decimal("100")


def test_find_unknown_transaction_raises(transaction_repo):
    with pytest.raises(NotFoundError):
        transaction_repo.find_by_id(1)


def test_transactions_come_back_newest_first(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(1)))
    transaction_repo.add(Transaction(2, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(10)))
    transaction_repo.add(Transaction(3, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(5)))
    assert [t.transaction_id for t in transaction_repo.list_all()] == [2, 3, 1]


def test_account_filter_matches_all_three_transaction_shapes(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(1)))
    transaction_repo.add(Transaction(2, TransactionType.WITHDRAWAL, Decimal("10"), from_account=1001, timestamp=at(2)))
    transaction_repo.add(Transaction(3, TransactionType.TRANSFER, Decimal("10"), from_account=1001, to_account=2001, timestamp=at(3)))
    transaction_repo.add(Transaction(4, TransactionType.DEPOSIT, Decimal("10"), to_account=9999, timestamp=at(4)))

    found = {t.transaction_id for t in transaction_repo.list_all(account_numbers=[1001])}
    assert found == {1, 2, 3}


def test_transfer_matching_both_sides_is_returned_once(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.TRANSFER, Decimal("10"),
                                     from_account=1001, to_account=2001, timestamp=at(1)))
    results = transaction_repo.list_all(account_numbers=[1001, 2001])
    assert [t.transaction_id for t in results] == [1]


def test_start_date_boundary_is_inclusive(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(5)))
    assert len(transaction_repo.list_all(start_date=at(5))) == 1


def test_end_date_boundary_is_inclusive(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(5)))
    assert len(transaction_repo.list_all(end_date=at(5))) == 1


def test_date_range_excludes_transactions_outside_it(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(1)))
    transaction_repo.add(Transaction(2, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(5)))
    transaction_repo.add(Transaction(3, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(20)))
    found = {t.transaction_id for t in transaction_repo.list_all(start_date=at(2), end_date=at(10))}
    assert found == {2}


def test_filter_by_transaction_type(transaction_repo):
    transaction_repo.add(Transaction(1, TransactionType.DEPOSIT, Decimal("10"), to_account=1001, timestamp=at(1)))
    transaction_repo.add(Transaction(2, TransactionType.TRANSFER, Decimal("10"), from_account=1001, to_account=2001, timestamp=at(2)))
    found = transaction_repo.list_all(transaction_type=TransactionType.TRANSFER)
    assert [t.transaction_id for t in found] == [2]


def test_transaction_repository_has_no_save_method(transaction_repo):
    assert not hasattr(transaction_repo, "save")


def test_generated_transaction_ids_are_ten_digits(transaction_repo):
    for _ in range(50):
        assert 1_000_000_000 <= transaction_repo.generate_transaction_id() <= 9_999_999_999


# ---------- ABC enforcement ----------

def test_incomplete_repository_implementation_cannot_be_instantiated():
    class BrokenBranchRepository(BranchRepository):
        def add(self, branch):
            pass

        def list_all(self, staff_over=None):
            return []
        # find_by_code deliberately missing

    with pytest.raises(TypeError):
        BrokenBranchRepository()
