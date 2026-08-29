from fastapi import APIRouter

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("")
def create_account():
    return {"detail": "TODO: open account"}


@router.get("")
def list_accounts():
    return {"detail": "TODO: list accounts"}


@router.get("/{account_number}")
def get_account(account_number: int):
    return {"detail": f"TODO: get account {account_number}"}


@router.delete("/{account_number}")
def delete_account(account_number: int):
    return {"detail": f"TODO: deactivate account {account_number}"}
