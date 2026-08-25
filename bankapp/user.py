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
    Still need to figure out what attributes to give to admin.
    '''

class Customer(User):
    '''
    It will extend from User for username and password.
    Has its own customer specific attributes.
    Its special attributes are needed to create customer elements.
    '''
    def __init__(self, customer_id: int, name: str, email: str, branch_id: int, username: str, password: str):
        super().__init__(username, password)
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.accounts = []
        self.branch_id = branch_id

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{classname}({self.customer_id}, {self.name}, {self.email}, {self.username})"

'''
USERS = []:
It is supposed to be the hardcoded user objects of the application.
Here we have 1 admin user object and 3 customer user objects.
'''
USERS = [
    Admin("admin1", "admin123!"),
    Customer(97, "Uzair", "Uzair@outlook.com",
             12345, "Uzair1", "Uzair123!"),
    Customer(98, "Tom", "tomcruise@gmail.com",
             45678, "TomCruise", "TomCruise321!"),
    Customer(99, "Steve", "steveirvin@me.com",
             67890, "Steve2", "Steve2123!")
]