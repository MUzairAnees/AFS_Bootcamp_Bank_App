from abc import ABC, abstractmethod

from app.exceptions import NotFoundError
from app.models.user import Customer


class CustomerRepository(ABC):
    '''
    CustomerRepository(ABC):
    Contract for customer storage. Any implementation - in-memory now,
    MongoDB in Phase 12 - must provide every method below.

    Two different scoping rules apply here, deliberately:

    - list_all() defaults to active customers only, since a deactivated
      customer should not appear in normal listings.
    - find_by_id(), exists() and username_exists() ignore is_active entirely.
      A deactivated customer still has to be readable by id, and its
      customer_id and username must stay permanently claimed so they are
      never reissued to somebody else.
    '''

    @abstractmethod
    def add(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def find_by_id(self, customer_id: int) -> Customer:
        pass

    @abstractmethod
    def list_all(self, branch_id: int | None = None,
                 include_inactive: bool = False) -> list[Customer]:
        pass

    @abstractmethod
    def exists(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        pass


class InMemoryCustomerRepository(CustomerRepository):
    '''
    Stores customers in a dict keyed by customer_id.
    '''

    def __init__(self):
        self._customers: dict[int, Customer] = {}

    def add(self, customer: Customer) -> None:
        self._customers[customer.customer_id] = customer

    def save(self, customer: Customer) -> None:
        self._customers[customer.customer_id] = customer

    def find_by_id(self, customer_id: int) -> Customer:
        customer = self._customers.get(customer_id)
        if customer is None:
            raise NotFoundError("Customer not found")
        return customer

    def list_all(self, branch_id: int | None = None,
                 include_inactive: bool = False) -> list[Customer]:
        customers = list(self._customers.values())
        if not include_inactive:
            customers = [c for c in customers if c.is_active]
        if branch_id is not None:
            customers = [c for c in customers if c.branch_id == branch_id]
        return customers

    def exists(self, customer_id: int) -> bool:
        return customer_id in self._customers

    def username_exists(self, username: str) -> bool:
        return any(c.username == username for c in self._customers.values())
