from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.controllers import accounts, branches, customers, transactions
from app.dependencies import (
    get_account_repository,
    get_branch_repository,
    get_customer_repository,
)
from app.seed import seed_accounts, seed_branches, seed_customers


def load_seed_data() -> None:
    '''
    Populates the running server's repositories with seed data.
    Admins are deliberately not loaded -> no endpoints read them in this module.
    '''
    customer_repository = get_customer_repository()
    for customer in seed_customers():
        customer_repository.add(customer)

    account_repository = get_account_repository()
    for account in seed_accounts():
        account_repository.add(account)

    branch_repository = get_branch_repository()
    for branch in seed_branches():
        branch_repository.add(branch)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_seed_data()
    yield


app = FastAPI(title="AFS Banking API", version="0.1.0", lifespan=lifespan)

app.include_router(customers.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")
app.include_router(branches.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
