from fastapi import APIRouter

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("")
def create_customer():
    return {"detail": "TODO: create customer"}


@router.get("")
def list_customers():
    return {"detail": "TODO: list customers"}


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    return {"detail": f"TODO: get customer {customer_id}"}


@router.put("/{customer_id}")
def update_customer(customer_id: int):
    return {"detail": f"TODO: update customer {customer_id}"}


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    return {"detail": f"TODO: deactivate customer {customer_id}"}
