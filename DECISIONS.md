# AI Management Decisions:

### Note: All code until the decisions below were built and verified personally without AI-assistance. Extra smoke tests created through AI-assisted development to confirm applications build status.

---
## transaction.py decisions - completed:

### My plan:
-The transaction object when built will generate a random 6 digit int as the transaction id.
-Transaction type is linked to determined by the type of call done through the customer dashboard. Only succeeds when the transaction succeeds.
-Transaction amount will work the same way. Determined by the type of call done through the customer dashboard. Only succeeds in holding the amount when the transaction succeeds.
-The to_account will be populated by the account that is chosen through the customer deposit transaction option, from_account will be None when only deposit option is chosen.
-The from_account will be populated by the account that is chosen through the customer withdraw transaction option, to_account will be None when only withdraw option is chosen.
-Both from_account and to_account are populated when the accounts are chosen and customer transfer option completes successfully. Amount is also determined when successfully inputed.


### AI Management plan - building transaction.py + implementing transactions:
Restating both, as requested — flagging where something is confirmed vs. still just an example, so you can correct anything before we touch code.

Plan for incorporating the Transaction class:
Bank.__init__ gets self.transactions = [] — the single log, owned by Bank, not by individual Accounts.


Bank._generate_transaction_id() — generates a random 10-digit int (1,000,000,000–9,999,999,999), checks it against every transaction_id already in self.transactions, regenerates on collision. Transaction itself never generates its own id — it's just handed one.


Deposits/withdrawals get routed through Bank, not called directly on the Account object from main.py. So Bank gains deposit(account, amount) and withdraw(account, amount) methods; transfer() already exists and gets extended, not replaced.


Success-gated construction: inside each of those Bank methods, the underlying Account.deposit()/withdraw() call happens first (it can raise ValueError/InsufficientFundsError). Only if that call doesn't raise does Bank construct a Transaction and append it to self.transactions. A failed attempt never produces a log entry.


Transaction.type is set by which Bank method was called (TransactionType.DEPOSIT / .WITHDRAWAL / .TRANSFER), not inferred after the fact.


from_account/to_account are account.account_number (int), never the Account object — matching the codebase's existing ID-reference convention.


main.py changes: customer_dashboard() cases "2" (deposit) and "3" (withdraw) switch from calling account_to_deposit.deposit(amount) directly to calling bank.deposit(account_to_deposit, amount). Case "4" (transfer) already calls bank.transfer(...), so its call site shape doesn't change — only Bank.transfer()'s internals gain the logging step.


Sequencing: one dashboard option wired at a time, in the order you choose, with you testing after each before we move to the next.

### AI Management plan - "View Transactions" (customer dashboard):
-New Bank method — filters self.transactions for a given customer. Exact name to be decided at implementation time, but it lives on Bank, consistent with find_customer/find_account/transfer.

-Filter logic: build the set of account_numbers from customer.accounts, then return every Transaction where from_account or to_account is in that set.

-Scope: all of the customer's accounts combined into one list — no per-account selection step (matches how option "1" already shows all accounts together).

-Display order: newest first — the filtered list gets reversed before printing (or iterated in reverse), so the most recent transaction shows at the top.

-Differentiation: no extra formatting needed — Transaction.__repr__ already prints transaction_id, type, amount, from_account, to_account, and timestamp, which is enough to tell entries apart.

-Empty state: if the filtered list is empty, print "No transactions yet." — same pattern as option "1"'s "No accounts created.".

-Menu changes in customer_dashboard():
--Printed menu becomes: 1) View your accounts / 2) Deposit / 3) Withdraw / 4) Transfer / 5) View transactions / 6) Exit
--case "5": → new "View transactions" logic
--case "6": → existing "Exit" logic (moved from "5")

-Admin dashboard untouched — this is customer-side at the moment.

Build order stays incremental: Bank method first (tested standalone in console) → then main.py menu wiring (tested live in the app). No implementation until you say go.

### AI Management plan - "View Transactions" (admin dashboard):
-No Bank changes — get_transactions() already handles the unfiltered case; this is main.py-only wiring.

-Header text: "All transactions:" (confirmed as-is).

-Empty-state text: "No transactions at this bank yet." (updated from the customer-side wording, per your correction).

-Menu renumbering:

| Current | New | Item |
|---|---|---|
| `"1"` | `"1"` | View all customers *(unchanged)* |
| `"2"` | `"2"` | View all accounts *(unchanged)* |
| — | **`"3"`** | **View all transactions** *(new)* |
| `"3"` | `"4"` | Add a customer |
| `"4"` | `"5"` | Delete a customer |
| `"5"` | `"6"` | Update a customer |
| `"6"` | `"7"` | Exit |

-Inline comment added to new case "3", matching the style already used on cases "1"/"2".
New case "3" body:

-Post-wiring validation (before any git push): a live-app pass through the entire renumbered menu, not just the new option — since a mislabeled case number would silently break existing logic. Checklist:
"1" View all customers — unchanged, sanity check only
"2" View all accounts — unchanged, sanity check only
"3" View all transactions — new: verify empty-state wording on a fresh bank, then verify it shows bank-wide activity after some customer transactions
"4" Add a customer — was "3"
"5" Delete a customer — was "4"
"6" Update a customer — was "5" (including its nested sub-menu, unaffected by the outer renumbering but worth re-confirming it still behaves)
"7" Exit — was "6"
case _: — still catches genuinely invalid input (e.g. "8", "0") correctly

---
## branch.py decisions - complete:

### AI Management plan - Complete Branch class/branch.py implementation
Final restated plan — Branch implementation
1. Admin gets admin_id: int. No generator needed (admins are only ever seeded, never created dynamically). 5 admins seeded with admin_id 1001–1005.

2. USERS seed data: 1 admin → 5 admins, each with a unique 4-digit admin_id (1001–1005), one per branch.

3. Branch scaffold finalized: Branch(branch_code: int, location: str, manager_id: int, staff: int = 0) — location is one of 5 fixed strings (Austin, Houston, San Antonio, Tampa, Maui), staff is a plain int headcount (not a list).

4. Bank gets branch plumbing:
self.branches = []
add_branch(branch) — seeding only, mirrors add_user/add_account
find_branch(branch_code) — raises NotFoundError like find_customer/find_account, used for validating admin input

5. 5 Branch instances seeded in create_bank(), branch_code 1–5, manager_id matching each admin's admin_id (1001–1005), staff given some seed headcount per branch.

6. Existing seeded Customers' branch_id values overwritten — Uzair/Tom/Steve move from the old arbitrary placeholders (12345/45678/67890) to real branch_codes (1–5).

7. Three Bank business-logic methods:
get_branch_customers(branch) — customers + their accounts at that branch
get_branch_transaction_volume(branch) — sum of .amount across every Transaction touching that branch's accounts (all-time; month filtering explicitly deferred to a future refactor)
get_branches_over_staff_ratio(limit) — every Branch where staff > limit

Restated plan — from here through the end of Branch
9. Build choose_branch(bank) helper in main.py.
Lives alongside choose_account() in the #-----------------------helper functions------------------------# section. Lists the 5 branches, prompts for a branch code, validates via read_int() (non-int → "Invalid input") plus bank.find_branch() (valid-int-but-not-1–5 → not found), returns the Branch or None. Reuses find_branch()'s existing NotFoundError rather than re-implementing a manual scan — this is the single shared piece all five downstream consumers need.

10. Admin dashboard menu shift — insert 3 new view-only options for the business-logic methods, grouped with the existing view-only options (1–3) rather than scattered among the mutation options. Proposed order (open to your adjustment when we get there):

11. Wire the 3 new options, one at a time, same discipline as everything else — each gets its own preview → green light → build → test cycle:
4 → choose_branch() then bank.get_branch_customers(branch)
5 → choose_branch() then bank.get_branch_transaction_volume(branch)
6 → prompt for a limit (int), then bank.get_branches_over_staff_ratio(limit)
Each needs its own empty-state message, matching the pattern used everywhere else in the app.

12. Add-customer branch validation — case "7" (post-shift)'s branch_id = read_int(...) free-entry gets replaced with choose_branch()-based bounded selection.

13. Update-customer branch validation — nested sub-choice "3" (Branch ID) gets the same bounded selection, plus the previously-confirmed "branch already set" vs "Customer updated." messaging depending on whether the pick matches the customer's current branch_id.
**Build order (sequential, one step per green light — same as always)

1. Admin.admin_id + USERS seed expansion
2. Branch scaffold finalized in branch.py
3. Bank.branches / add_branch() / find_branch()
4. Seed the 5 Branches in create_bank()
5. Overwrite the 3 existing customers' branch_ids
6. The 3 business-logic methods on Bank
7. main.py Add-customer branch validation
8. main.py Update-customer branch validation
9. main.py new admin menu option for the staff-ratio query**

---
## Extra logic decisions - completed
### AI Management plan - Extras design plan
Current design plan — 6 items

1. Bank._generate_account_number() (dependency for items 2 and 3)
Random 4-digit int (1000–9999), deduped against every existing account_number in self.accounts, regenerating on collision. Same pattern as _generate_transaction_id(), narrower range. Lives in bank.py's account section.

2. New customers start with a CheckingAccount
When an admin adds a customer (admin case "7"), a CheckingAccount is created automatically: account_number from _generate_account_number(), owner_id = the new customer's id, balance 0. Wired via existing bank.add_account(), which links it to the owner.

3. Customers can add accounts
New customer dashboard menu option — prompts for account type (Savings/Checking), creates it with a generated account_number, owner_id = that customer, balance 0. No deletion; unlimited accounts. Requires a customer menu shift (Exit moves from "6" to "7").

4. customer_id must be strictly > 0
In the admin add-customer flow, reject 0 and negatives with a re-prompt.

5. Transfer prompts get distinct headers
choose_account() gains an optional header parameter (default preserves current text for deposit/withdraw). Transfer passes "Accounts available to withdraw from:" for the first pick and "Accounts available to deposit into:" for the second. Selection logic unchanged.

6. Seed account type flip — seed.py only, two lines:

ACCOUNTS = [
    SavingsAccount(1001, 97, Decimal("1000")),
    CheckingAccount(1002, 98, Decimal("99000")),
    CheckingAccount(1003, 99, Decimal("59000")),
    CheckingAccount(2001, 97, Decimal("900")),
]

Dependency note: items 2 and 3 both require item 1 first. Items 4, 5, and 6 are independent of everything else and can go in any order.

Build order: 6, 1, 2, 3, 4, 5.

---
## Application testing plan - edge cases, through each aspect, sequentially - Completed
### AI Management plan - Overall Testing plan
Testing plan:

Since we've already covered happy-path and basic failure-path testing extensively during the build, this pass targets boundaries, extremes, and malformed input specifically — the things a "does it work" test doesn't naturally hit. Proposed order, foundational → integrated:

1. Input validation helpers (read_int, read_amount) — malformed/boundary input: empty string, whitespace-only, float strings passed to read_int, comma-formatted numbers, scientific notation, extra whitespace, huge numbers.
2. Account deposit/withdraw boundaries — exact-zero amounts, withdrawing the exact balance, the exact overdraft boundary (-500 vs -500.01), fractional-cent Decimal precision, very large amounts.
3. Transaction ledger integrity at scale — many transactions in one session, ID uniqueness holding under real volume (not just mocked collisions), get_transactions() for a customer with zero accounts. 
4. Branch business-logic boundaries — exact staff-ratio limit edge, a branch with multiple customers aggregating correctly, transaction volume for a branch with zero activity vs. failed-only attempts. 
5. Customer/account lifecycle edge cases — remove_customer() with multiple accounts (does it clean all of them out of bank.accounts, not just customer.accounts?), re-adding a customer_id after deletion, admin updating a customer with zero accounts. 
6. Account creation under real collision pressure — creating dozens of accounts in one session (both auto- and customer-created) to stress _generate_account_number()'s dedup loop against actual accumulated state, not a mocked scenario. 
7. Login/auth edge cases — wrong password, unknown username, case sensitivity, empty credentials. 
8. Full end-to-end integration smoke test — one long continuous session touching every menu option across both dashboards.

Test 1 Results to Fix:
1. '1e3' scientific notation accepted as an amount -Yes- This is the one I'd actually flag as worth fixing. Decimal("1e3") stores as Decimal('1E+3'), and nothing in the app normalizes it — if a customer deposits 1e3, their account's __repr__ would print the balance as 1E+3 instead of 1000 from then on, which is inconsistent with every other money display in the app.
2. '10.999' (3 decimal places) accepted -Medium- Similar issue — nothing quantizes deposits/withdrawals to 2 decimal places, so an odd-precision amount would persist in the balance and print as-is (10.999) rather than looking like currency.

Test 2 Results to Fix:
1. The sub-cent finding (0.001 accepted) is the same open question as Test 1's 10.999/scientific-notation findings — no rounding/quantization exists anywhere in the deposit/withdraw path. Worth treating as one fix decision, not two separate ones, since they're the same root gap (amounts aren't normalized to currency precision on the way in).

Test 3 Results to Fix:
None.

Test 4 Results to Fix:
None.

Test 5 Results to Fix:
None.

Test 6 Results to Fix:
None.

Test 7 Results to Fix:
1. No username-uniqueness check on customer creation — a duplicate username+password combination makes the second customer's account permanently unreachable via login, though the data itself stays intact -Real- you flagged this as the one to weigh most carefully.

Test 8 Results to Fix:
None.

----
### Completed console version of application, pair programmed with architect and code developer, Uzair Anees and Anthropic Claude.
