from decimal import Decimal

from app.models.account import Account, CheckingAccount, SavingsAccount
from app.models.branch import Branch
from app.models.user import Admin, Customer

'''
seed.py:
Holds all hardcoded seed data used to populate the repositories at startup.

Each function returns freshly constructed objects rather than exposing
module-level instances. Module 01 stored instances at module level, so every
load handed out the same objects and mutations leaked between them - the bug
that needed deepcopy to patch. Constructing new objects per call removes that
class of problem entirely instead of working around it.

seed_admins() is not loaded into a repository in this module. Admins have no
endpoints and no authentication yet; the data is here so the manager_id values
referenced by Branch objects are traceable, and so Module 04 has them ready.
'''


def seed_admins() -> list[Admin]:
    return [
        Admin(1001, "admin1", "admin123!"),
        Admin(1002, "admin2", "admin223!"),
        Admin(1003, "admin3", "admin323!"),
        Admin(1004, "admin4", "admin423!"),
        Admin(1005, "admin5", "admin523!"),
    ]


def seed_customers() -> list[Customer]:
    return [
        Customer(97, "Uzair", "Uzair@outlook.com", 1, "Uzair1", "Uzair123!"),
        Customer(98, "Tom", "tomcruise@gmail.com", 2, "TomCruise", "TomCruise321!"),
        Customer(99, "Steve", "steveirvin@me.com", 3, "Steve2", "Steve2123!"),
    ]


def seed_accounts() -> list[Account]:
    return [
        SavingsAccount(1001, 97, Decimal("1000")),
        CheckingAccount(1002, 98, Decimal("99000")),
        CheckingAccount(1003, 99, Decimal("59000")),
        CheckingAccount(2001, 97, Decimal("900")),
    ]


def seed_branches() -> list[Branch]:
    return [
        Branch(1, "Austin", 1001, 6),
        Branch(2, "Houston", 1002, 9),
        Branch(3, "San Antonio", 1003, 4),
        Branch(4, "Tampa", 1004, 11),
        Branch(5, "Maui", 1005, 2),
    ]
