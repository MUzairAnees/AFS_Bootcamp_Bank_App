class Branch:
    '''
    Branch():
    Represents a single bank branch location.
    Directly instantiable -> unlike User/Account, Branch has no subtypes,
    so it's a plain data holder rather than an ABC with children.

    Attributes:
    branch_code: unique identifier for this branch, sequential 1-5.
    Matches the branch_id values stored on Customer objects (user.py).

    location: str, the city the branch is in. One of five fixed values:
    Austin, Houston, San Antonio, Tampa, Maui.

    manager_id: int, the admin_id of the Admin managing this branch.
    Stored as an id (not an Admin reference) to match the ID-based linking
    style used elsewhere (Account.owner_id, Customer.branch_id).
    Every branch has exactly one manager.

    staff: int, the headcount of staff working at this branch.
    Since every branch has exactly one manager, this doubles as the
    branch's staff-to-manager ratio.
    '''

    def __init__(self, branch_code: int, location: str, manager_id: int, staff: int = 0):
        self.branch_code = branch_code
        self.location = location
        self.manager_id = manager_id
        self.staff = staff

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{classname}({self.branch_code}, {self.location}, manager={self.manager_id}, staff={self.staff})"
