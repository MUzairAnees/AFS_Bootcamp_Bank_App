from abc import ABC, abstractmethod

from app.exceptions import NotFoundError
from app.models.branch import Branch


class BranchRepository(ABC):
    '''
    BranchRepository(ABC):
    Contract for branch storage. Any implementation - in-memory now,
    MongoDB in Phase 12 - must provide every method below.

    Branches are read-only in this API: they are seeded once and never
    created, edited, or removed through an endpoint. add() exists only
    so seed data can be loaded.

    list_all() accepts its filter rather than returning everything for a
    caller to filter -> lets the storage layer satisfy the query however it
    can, e.g. a MongoDB query instead of loading every record into memory.

    staff_over is named for its strict > comparison: the spec asks for
    branches "over a specified limit", so a branch with exactly that many
    staff is excluded. Deliberately not called min_staff, which would imply
    >= and read inconsistently against AccountRepository's min_balance.
    '''

    @abstractmethod
    def add(self, branch: Branch) -> None:
        pass

    @abstractmethod
    def list_all(self, staff_over: int | None = None) -> list[Branch]:
        pass

    @abstractmethod
    def find_by_code(self, branch_code: int) -> Branch:
        pass


class InMemoryBranchRepository(BranchRepository):
    '''
    Stores branches in a dict keyed by branch_code.
    A dict rather than a list -> lookups are direct instead of scans,
    which mirrors how the MongoDB implementation will index on _id.
    '''

    def __init__(self):
        self._branches: dict[int, Branch] = {}

    def add(self, branch: Branch) -> None:
        self._branches[branch.branch_code] = branch

    def list_all(self, staff_over: int | None = None) -> list[Branch]:
        branches = list(self._branches.values())
        if staff_over is not None:
            branches = [branch for branch in branches if branch.staff > staff_over]
        return branches

    def find_by_code(self, branch_code: int) -> Branch:
        branch = self._branches.get(branch_code)
        if branch is None:
            raise NotFoundError("Branch not found")
        return branch
