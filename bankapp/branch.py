class Branch:
    '''
    Branch():
    Represents a single bank branch location.
    Directly instantiable -> unlike User/Account, Branch has no subtypes,
    so it's a plain data holder rather than an ABC with children.

    Attributes:
    branch_code: unique identifier for this branch. Matches the branch_id
    values already stored on Customer objects (user.py).

    location: str, physical address/city of the branch.

    manager_id: int, the id of the staff member managing this branch.
    Stored as an id (not a User/Admin reference) to match the ID-based
    linking style already used elsewhere (Account.owner_id, Customer.branch_id).

    staff: list of staff member ids (int) working at this branch.
    Empty list by default.
    '''

    def __init__(self, branch_code: int, location: str, manager_id: int, staff: list[int] = None):
        self.branch_code = branch_code
        self.location = location
        self.manager_id = manager_id
        self.staff = staff if staff is not None else []

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        return f"{classname}({self.branch_code}, {self.location}, manager={self.manager_id}, staff={self.staff})"
