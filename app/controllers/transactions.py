from fastapi import APIRouter

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/deposit")
def deposit():
    return {"detail": "TODO: deposit"}


@router.post("/withdraw")
def withdraw():
    return {"detail": "TODO: withdraw"}


@router.post("/transfer")
def transfer():
    return {"detail": "TODO: transfer"}


@router.get("")
def list_transactions():
    return {"detail": "TODO: list transactions"}


@router.get("/{transaction_id}")
def get_transaction(transaction_id: int):
    return {"detail": f"TODO: get transaction {transaction_id}"}
