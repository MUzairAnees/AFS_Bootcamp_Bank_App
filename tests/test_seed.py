from decimal import Decimal

from app.models.account import CheckingAccount, SavingsAccount
from app.seed import seed_accounts, seed_admins, seed_branches, seed_customers


# ---------- Fresh objects per call ----------

def test_seed_customers_returns_new_objects_each_call():
    first = seed_customers()
    second = seed_customers()
    assert first[0] is not second[0]


def test_mutating_seeded_data_does_not_affect_a_later_call():
    first = seed_customers()
    first[0].name = "MUTATED"
    assert seed_customers()[0].name == "Uzair"


def test_seed_accounts_returns_new_objects_each_call():
    first = seed_accounts()
    second = seed_accounts()
    assert first[0] is not second[0]


def test_mutating_a_seeded_balance_does_not_affect_a_later_call():
    account = seed_accounts()[0]
    account.deposit(Decimal("500"))
    assert seed_accounts()[0].balance == Decimal("1000")


def test_seed_branches_returns_new_objects_each_call():
    assert seed_branches()[0] is not seed_branches()[0]


# ---------- Contents ----------

def test_five_admins_are_seeded():
    assert [a.admin_id for a in seed_admins()] == [1001, 1002, 1003, 1004, 1005]


def test_three_customers_are_seeded_and_active():
    customers = seed_customers()
    assert {c.customer_id for c in customers} == {97, 98, 99}
    assert all(c.is_active for c in customers)


def test_customers_are_spread_across_branches():
    assert {c.customer_id: c.branch_id for c in seed_customers()} == {97: 1, 98: 2, 99: 3}


def test_account_types_are_one_savings_and_three_checking():
    accounts = seed_accounts()
    savings = [a for a in accounts if isinstance(a, SavingsAccount)]
    checking = [a for a in accounts if isinstance(a, CheckingAccount)]
    assert len(savings) == 1
    assert len(checking) == 3


def test_seeded_accounts_are_active_with_expected_balances():
    balances = {a.account_number: a.balance for a in seed_accounts()}
    assert balances == {
        1001: Decimal("1000"),
        1002: Decimal("99000"),
        1003: Decimal("59000"),
        2001: Decimal("900"),
    }
    assert all(a.is_active for a in seed_accounts())


def test_five_branches_are_seeded_with_expected_staff():
    staff = {b.branch_code: b.staff for b in seed_branches()}
    assert staff == {1: 6, 2: 9, 3: 4, 4: 11, 5: 2}


# ---------- Referential integrity ----------

def test_every_branch_manager_maps_to_a_seeded_admin():
    admin_ids = {a.admin_id for a in seed_admins()}
    manager_ids = {b.manager_id for b in seed_branches()}
    assert manager_ids <= admin_ids


def test_every_account_owner_maps_to_a_seeded_customer():
    customer_ids = {c.customer_id for c in seed_customers()}
    owner_ids = {a.owner_id for a in seed_accounts()}
    assert owner_ids <= customer_ids


def test_every_customer_branch_maps_to_a_seeded_branch():
    branch_codes = {b.branch_code for b in seed_branches()}
    customer_branches = {c.branch_id for c in seed_customers()}
    assert customer_branches <= branch_codes


def test_seeded_ids_are_unique_within_each_collection():
    assert len({c.customer_id for c in seed_customers()}) == len(seed_customers())
    assert len({a.account_number for a in seed_accounts()}) == len(seed_accounts())
    assert len({b.branch_code for b in seed_branches()}) == len(seed_branches())
    assert len({a.admin_id for a in seed_admins()}) == len(seed_admins())
