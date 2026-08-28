# AFS Banking App

A console-based banking application built as a learning project for the AFS Bootcamp, focused on Object-Oriented Design (OOD) fundamentals in Python.

> **Note:** This is currently a console-only (CLI) application. There is no web, GUI, or API interface at this time.

## About

Built for practice by Uzair, working through OOD, business-logic design, and iterative development with an AI coding assistant.

## Module 01 — Fundamentals: OOD, Vibe Coding & Logic Building

Module 01 is complete. The application models a small multi-branch bank with customers, accounts, transactions, and branches, accessed through separate Admin and Customer console dashboards.

### Domain model
- **User** (abstract) → **Admin**, **Customer**
- **Account** (abstract) → **SavingsAccount**, **CheckingAccount**
- **Transaction** — records every deposit, withdrawal, and transfer
- **Branch** — one of five fixed locations, each with a manager and staff count

### Customer-centric methods
Available through the Customer dashboard:
- View own accounts
- Deposit into an account
- Withdraw from an account
- Transfer funds between own accounts
- View own transaction history
- Open a new account (Savings or Checking, unlimited, no deletion)

### Admin-centric methods
Available through the Admin dashboard:
- View all customers
- View all accounts
- View all transactions (bank-wide)
- Add a customer (auto-provisions a starter Checking account)
- Delete a customer
- Update a customer's details

### Filtering & searching methods
Query methods used across both dashboards to look up and aggregate data:
- Find a customer, account, or branch by ID
- View a customer's transactions, or the entire bank's
- View all customers (and their accounts) at a given branch
- View a branch's total transaction volume
- View every branch exceeding a given staff-to-manager ratio
- Check whether a username is already taken

### Known deviations from the original spec
A few requirements were deliberately scoped out to keep the account model simple and the codebase easy to follow end-to-end, rather than chasing every literal requirement:

- **Savings account minimum balance** — enforced at a fixed $0 floor rather than a configurable minimum.
- **Transaction volume per month** — the volume query reports all-time totals; month-level filtering was left for a future pass, since the underlying transaction timestamps already support it.
- **Branch staff** — modeled as a headcount (int) rather than a list of individual staff members, since no separate "staff" user type exists in the domain and every branch has exactly one manager.

These were conscious choices made to keep the application good enough and easy to follow, not oversights.
