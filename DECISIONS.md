# AI Management Plans - Mohamed Uzair Anees + Claude Code

## Module 02 — Restated Plan
### Architecture

Fresh branch off main; domain files copied verbatim from console-version as each phase needs them.

Layered: controllers/ → services/ → repositories/ → models/ + schemas/.
bank.py dissolves; main.py becomes the FastAPI bootstrap.

In-memory repositories first, MongoDB Atlas swap at the end of the module.

### API design decisions
Staff-facing API — no customer/admin split, no auth in Module 02.

Style B filtering — flat collections + query params (/customers?branch_id=1), never nested resource paths. Exception: /branches/{id}/transaction-volume (computed aggregate).

Branches read-only — no create/update/delete.

Soft delete for customers and accounts via is_active; standalone DELETE /accounts/{id} included.

Active-only by default on all lists, ?include_inactive= to opt in.

200 with is_active: false for deactivated records — never 404.

Uniqueness checks span inactive records (so customer_id is never reused); everything else defaults to active-only.

Inactive accounts reject transactions with 409.

No reactivation in Module 02.

PUT = partial update via all-optional schema.

Decimal serialized as string; read_amount() validation becomes schema validators returning 400.

Transaction filtering: start_date/end_date range, inclusive boundaries, case-insensitive type, UTC throughout.

MongoDB: business IDs used as _id (option B), collision handled at insert.

Customer.accounts dropped — accounts queried by owner_id.

Admin ported as data-only — no endpoints, keeps Branch.manager_id meaningful and gives Module 04 auth a foundation.

Seeding: startup hook during in-memory phase → script when Mongo lands. Optional dev-only reset endpoint behind an env flag.

## Phase sequence
###	Phase
1. Environment & FastAPI bootstrap + /health 
2. Directory skeleton + all endpoints stubbed 
3. Foundation: domain models ported, in-memory repositories, startup seed 
4. Branches (read-only — first full vertical slice)
5. Customer CREATE 
6. Customer READ 
7. Customer UPDATE 
8. Accounts (create, read, filtering, soft delete)
9. Customer DELETE (soft, cascades to accounts)
10. Transactions (deposit/withdraw/transfer, read, filtering)
11. Cross-resource rules & polish 
12. MongoDB Atlas swap

## Per-phase workflow
1. Phase preview 
2. Test focus preview 
3. Your green light 
4. Implementation 
5. Test script preview

You run it, report results — no advancing until confirmed

---

## Pre-phase:
One choice worth naming: I listed only your direct dependencies rather than the full 27-line freeze. pip resolves the transitive ones (starlette, pydantic, anyio, and the uvicorn[standard] extras like watchfiles/websockets) automatically. Far more readable and maintainable; the tradeoff is slightly less exact reproducibility than a full pin. If you'd rather have every transitive version locked, say so and I'll expand it.

Going forward:

Development: pip install -r requirements-dev.txt
Deployment (Module 05): pip install -r requirements.txt