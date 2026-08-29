from fastapi import APIRouter

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("")
def list_branches():
    return {"detail": "TODO: list branches"}


@router.get("/{branch_code}")
def get_branch(branch_code: int):
    return {"detail": f"TODO: get branch {branch_code}"}


@router.get("/{branch_code}/transaction-volume")
def get_branch_transaction_volume(branch_code: int):
    return {"detail": f"TODO: transaction volume for branch {branch_code}"}
