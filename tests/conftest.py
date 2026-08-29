import pytest

from app.repositories.account_repository import InMemoryAccountRepository
from app.repositories.branch_repository import InMemoryBranchRepository
from app.repositories.customer_repository import InMemoryCustomerRepository
from app.repositories.transaction_repository import InMemoryTransactionRepository
from app.seed import seed_accounts, seed_branches, seed_customers

'''
conftest.py:
Shared pytest fixtures. Anything defined here is available to every test file
without importing it.

Each fixture builds a fresh, independently seeded repository. pytest runs
fixtures per test function, so no test can see another test's data.

Phase 4 adds TestClient fixtures here that wire these repositories into the app
through app.dependency_overrides.
'''


@pytest.fixture
def branch_repo():
    repo = InMemoryBranchRepository()
    for branch in seed_branches():
        repo.add(branch)
    return repo


@pytest.fixture
def customer_repo():
    repo = InMemoryCustomerRepository()
    for customer in seed_customers():
        repo.add(customer)
    return repo


@pytest.fixture
def account_repo():
    repo = InMemoryAccountRepository()
    for account in seed_accounts():
        repo.add(account)
    return repo


@pytest.fixture
def transaction_repo():
    return InMemoryTransactionRepository()
