from decimal import Decimal
from bankapp.user import Admin, Customer
from bankapp.account import SavingsAccount, CheckingAccount
from bankapp.branch import Branch

'''
seed.py:
Holds all hardcoded seed data used to populate a fresh Bank via create_bank().
Keeps class files (user.py, account.py, branch.py) focused purely on class
definitions, and keeps Bank/create_bank() focused on wiring, not data.
'''

USERS = [
    Admin(1001, "admin1", "admin123!"),
    Admin(1002, "admin2", "admin223!"),
    Admin(1003, "admin3", "admin323!"),
    Admin(1004, "admin4", "admin423!"),
    Admin(1005, "admin5", "admin523!"),
    Customer(97, "Uzair", "Uzair@outlook.com",
             1, "Uzair1", "Uzair123!"),
    Customer(98, "Tom", "tomcruise@gmail.com",
             2, "TomCruise", "TomCruise321!"),
    Customer(99, "Steve", "steveirvin@me.com",
             3, "Steve2", "Steve2123!")
]

ACCOUNTS = [
    SavingsAccount(1001, 97, Decimal("1000")),
    CheckingAccount(1002, 98, Decimal("99000")),
    CheckingAccount(1003, 99, Decimal("59000")),
    CheckingAccount(2001, 97, Decimal("900")),
]

BRANCHES = [
    Branch(1, "Austin", 1001, 6),
    Branch(2, "Houston", 1002, 9),
    Branch(3, "San Antonio", 1003, 4),
    Branch(4, "Tampa", 1004, 11),
    Branch(5, "Maui", 1005, 2),
]
