from abc import ABC


class User(ABC):
    '''
    General User class that is based on shared attributes used by both admin and customer.
    User class is not meant to be called directly.
    Called only through child classes.
    '''
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{classname}({self.username})"


class Admin(User):
    '''
    It will extend from User for username and password.
    Has its own admin specific attribute.
    admin_id doubles as the manager_id referenced by Branch objects -> every
    admin manages exactly one branch.

    Data-only in this API -> admins are seeded, never created or edited through
    an endpoint, and there is no authentication in this module.
    '''
    def __init__(self, admin_id: int, username: str, password: str):
        super().__init__(username, password)
        self.admin_id = admin_id

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{classname}({self.admin_id}, {self.username})"


class Customer(User):
    '''
    It will extend from User for username and password.
    Has its own customer specific attributes.

    Does not hold its own accounts -> the account repository owns that
    relationship, and a customer's accounts are looked up by owner_id.

    is_active supports soft deletion: deactivating a customer keeps the record,
    so financial history stays resolvable and a customer_id is never reused.
    '''
    def __init__(self, customer_id: int, name: str, email: str, branch_id: int,
                 username: str, password: str, is_active: bool = True):
        super().__init__(username, password)
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.branch_id = branch_id
        self.is_active = is_active

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{classname}({self.customer_id}, {self.name}, {self.email}, {self.username}, active={self.is_active})"
