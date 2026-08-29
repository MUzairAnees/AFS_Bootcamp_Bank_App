from app.repositories.account_repository import AccountRepository, InMemoryAccountRepository
from app.repositories.branch_repository import BranchRepository, InMemoryBranchRepository
from app.repositories.customer_repository import CustomerRepository, InMemoryCustomerRepository
from app.repositories.transaction_repository import (
    InMemoryTransactionRepository,
    TransactionRepository,
)

'''
dependencies.py:
Holds the single repository instance of each kind that the running server uses,
and the provider functions FastAPI calls to hand them to controllers.

Annotated with the ABC rather than the concrete class -> callers depend on the
contract, not on the fact that storage is currently in-memory. Phase 12 swaps
the four constructor calls below for MongoDB implementations and nothing else
changes.

Tests do not use these instances. They override the provider functions with
fresh repositories per test, which is what keeps one test from seeing another
test's data.
'''

_customer_repository: CustomerRepository = InMemoryCustomerRepository()
_account_repository: AccountRepository = InMemoryAccountRepository()
_transaction_repository: TransactionRepository = InMemoryTransactionRepository()
_branch_repository: BranchRepository = InMemoryBranchRepository()


def get_customer_repository() -> CustomerRepository:
    return _customer_repository


def get_account_repository() -> AccountRepository:
    return _account_repository


def get_transaction_repository() -> TransactionRepository:
    return _transaction_repository


def get_branch_repository() -> BranchRepository:
    return _branch_repository
