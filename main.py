from bankapp.bank import Bank, create_bank
from bankapp.user import User, Customer, Admin
from bankapp.account import *
from bankapp.exceptions import BankError, NotFoundError
from bankapp.branch import Branch
from decimal import Decimal, InvalidOperation

def main():
    '''
    Main():
    Acts as the entry point of the program.

    Purpose:
    0) Creates a bank to work with.
    1) Welcomes user -> welcome().
    2) Prompts for authorization -> login().
    2a) If authorization returns a specific val(stored in check var)
    -> activates the related x_dashboard() -> x == admin or cust.
    3) Exits program -> goodbye().
    '''

    bank = create_bank()

    welcome()

    #login() -> contains login logic and stores results in var
    login_res = login(bank)

    if isinstance(login_res, Admin):
        admin_dashboard(bank, login_res)
    elif isinstance(login_res, Customer):
        customer_dashboard(bank, login_res)
    else:
        print("\nLog in failed. Please try again later.")
        # moves to goodbye()

    goodbye()


#------------------------------------------------------------------------#


def welcome():
    '''
    Welcome():
    Prints welcome message
    '''
    print("---------------------------")
    print("--Welcome to AFS Banking!--")
    print("---------------------------\n")

def login(bank: Bank) -> User | None:
    '''
    Login():
    Asks user for username and password.
    Checks if username and password are in the system.
    Returns the User object if true else returns None
    '''
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    return bank.login(username, password)

def admin_dashboard(bank: Bank, admin: Admin):
    '''
    AdminDashboard():
    Contains a menu of what the admin can do.
    '''
    print(f"\nHello {admin.username}.")

    while True:
        choice = input("\nWhat would you like to do?\n"
                       "1) View all customers\n"
                       "2) View all accounts\n"
                       "3) View all transactions\n"
                       "4) View branch customers\n"
                       "5) View branch transaction volume\n"
                       "6) View branches over staff ratio\n"
                       "7) Add a customer\n"
                       "8) Delete a customer\n"
                       "9) Update a customer\n"
                       "10) Exit\n"
                       "Enter your choice: ")

        match choice:
            case "1":
                #Views bank users -> customers
                for user in bank.users:
                    if isinstance(user, Customer):
                        print(user)

            case "2":
                #Views all bank accounts
                for account in bank.accounts:
                    print(account)

            case "3":
                #Views all transactions bank-wide, regardless of customer
                all_transactions = bank.get_transactions()
                if not all_transactions:
                    print("No transactions at this bank yet.")
                else:
                    print("\nAll transactions:")
                    for transaction in all_transactions:
                        print(transaction)

            case "4":
                #Views all customers at a chosen branch, along with their accounts
                branch = choose_branch(bank)
                if branch is not None:
                    branch_customers = bank.get_branch_customers(branch)
                    if not branch_customers:
                        print(f"\nNo customers at {branch.location} yet.")
                    else:
                        print(f"\nCustomers at {branch.location}:")
                        for customer in branch_customers:
                            print(customer)
                            for account in customer.accounts:
                                print(f"   {account}")

            case "5":
                #Views the total transaction volume (all-time) for a chosen branch
                branch = choose_branch(bank)
                if branch is not None:
                    volume = bank.get_branch_transaction_volume(branch)
                    print(f"\nTotal transaction volume at {branch.location}: {volume}")

            case "6":
                #Views every branch whose staff-to-manager ratio exceeds a given limit
                limit = read_int("Please enter a staff ratio limit: ")
                branches_over_limit = bank.get_branches_over_staff_ratio(limit)
                if not branches_over_limit:
                    print(f"\nNo branches over a staff ratio of {limit}.")
                else:
                    print(f"\nBranches over a staff ratio of {limit}:")
                    for branch in branches_over_limit:
                        print(branch)

            case "7":
                #Adds customer based on customerID -> only if customerID doesn't exist.
                customer_id = read_int("Please enter customer id: ")
                while customer_id <= 0:
                    print("Customer id must be greater than 0.")
                    customer_id = read_int("Please enter customer id: ")
                try:
                    bank.find_customer(customer_id)
                    print("Customer ID already exists.")
                except NotFoundError:
                    branch = choose_branch(bank)
                    if branch is not None:
                        name = input("Please enter customer name: ")
                        email = input("Please enter customer email: ")
                        username = input("Please enter customer username: ")
                        while bank.username_exists(username):
                            print("Username already taken. Please choose a different username.")
                            username = input("Please enter customer username: ")
                        password = input("Please enter customer password: ")

                        new_customer = Customer(customer_id, name, email, branch.branch_code, username, password)
                        bank.add_user(new_customer)

                        new_account = CheckingAccount(bank._generate_account_number(), customer_id)
                        bank.add_account(new_account)

                        print(f"\nCustomer {name}, {customer_id} added.")
                        print(f"Checking account {new_account.account_number} created for {name}.")

            case "8":
                customer_to_delete_id = read_int("Please enter customer id: ")
                try:
                    bank.remove_customer(customer_to_delete_id)
                    print("\nCustomer deleted.")
                except NotFoundError:
                    print("Customer does not exist.")

            case "9":
                customer_id = read_int("Please enter customer id: ")
                try:
                    customer_to_update = bank.find_customer(customer_id)
                except NotFoundError:
                    print("Customer does not exist.")
                else:
                    print(f"Editing {customer_to_update.customer_id}: {customer_to_update.name}.")

                    print("\nWhat would you like to update?\n"
                          "1) Name\n"
                          "2) Email\n"
                          "3) Branch ID\n"
                          "4) Username\n"
                          "5) Password\n"
                          "6) No update needed anymore.\n")
                    choice = input("Please enter your choice: ")

                    match choice:
                        case "1":
                            customer_to_update.name = input("Please enter new customer name: ")
                            print("\nCustomer updated.")
                        case "2":
                            customer_to_update.email = input("Please enter new customer email: ")
                            print("\nCustomer updated.")
                        case "3":
                            branch = choose_branch(bank)
                            if branch is not None:
                                if branch.branch_code == customer_to_update.branch_id:
                                    print("\nBranch already set.")
                                else:
                                    customer_to_update.branch_id = branch.branch_code
                                    print("\nCustomer updated.")
                        case "4":
                            new_username = input("Please enter new customer username: ")
                            if new_username == customer_to_update.username:
                                print("\nUsername already set.")
                            elif bank.username_exists(new_username):
                                print("\nUsername already taken. Please choose a different username.")
                            else:
                                customer_to_update.username = new_username
                                print("\nCustomer updated.")
                        case "5":
                            customer_to_update.password = input("Please enter new customer password: ")
                            print("\nCustomer updated.")
                        case "6":
                            print("\nNo update needed anymore.")
                        case _:
                            print("Invalid choice. Please try again.")

            case "10":
                print("\nExiting dashboard...")
                break

            case _:
                print("\nInvalid choice. Please try again.")

def customer_dashboard(bank: Bank, customer: Customer):
    '''
    CustomerDashboard():
    Contains a menu of what the customer can do.
    '''
    print(f"\nHello {customer.name}!")

    while True:
        choice = input("\nWhat would you like to do?\n"
                       "1) View your accounts\n"
                       "2) Deposit an amount\n"
                       "3) Withdraw an amount\n"
                       "4) Transfer an amount between accounts\n"
                       "5) View transactions\n"
                       "6) Add an account\n"
                       "7) Exit\n"
                       "Enter your choice: ")

        match choice:
            case "1":
                if not customer.accounts:
                    print("No accounts created.")
                else:
                    print("\nYour accounts:")
                    for account in customer.accounts:
                        print(account)

            case "2":
                account_to_deposit = choose_account(customer)
                if account_to_deposit is not None:
                    amount = read_amount("How much would you like to deposit? ")
                    try:
                        bank.deposit(account_to_deposit, amount)
                        print(f"Deposited amount. New balance: {account_to_deposit.balance}")
                    except ValueError as e:
                        print(e)

            case "3":
                account_to_withdraw_from = choose_account(customer)
                if account_to_withdraw_from is not None:
                    amount = read_amount("How much would you like to withdraw? ")
                    try:
                        bank.withdraw(account_to_withdraw_from, amount)
                        print(f"Withdrew amount. New balance: {account_to_withdraw_from.balance}")
                    except (ValueError, BankError) as e:
                        print(e)

            case "4":
                from_account = choose_account(customer, header="Accounts available to withdraw from:")
                if from_account is not None:
                    to_account = choose_account(customer, header="Accounts available to deposit into:")

                    if to_account is None:
                        pass
                    elif from_account is to_account:
                        print("\nYou cannot transfer money from/to the same account!.")
                    else:
                        transfer_amount = read_amount("How much would you like to transfer? ")
                        try:
                            bank.transfer(from_account, to_account, transfer_amount)
                            print(f"Transferred amount. New balances: {from_account.balance}, {to_account.balance}")
                        except (ValueError, BankError) as e:
                            print(e)

            case "5":
                customer_transactions = bank.get_transactions(customer)
                if not customer_transactions:
                    print("No transactions yet.")
                else:
                    print("\nYour transactions:")
                    for transaction in customer_transactions:
                        print(transaction)

            case "6":
                #Adds a new account for this customer -> no deletion, unlimited accounts allowed
                account_type = input("\nWhat type of account would you like to open?\n"
                                      "1) Savings\n"
                                      "2) Checking\n"
                                      "Enter your choice: ")

                match account_type:
                    case "1":
                        new_account = SavingsAccount(bank._generate_account_number(), customer.customer_id)
                        bank.add_account(new_account)
                        print(f"\nSavings account {new_account.account_number} created.")
                    case "2":
                        new_account = CheckingAccount(bank._generate_account_number(), customer.customer_id)
                        bank.add_account(new_account)
                        print(f"\nChecking account {new_account.account_number} created.")
                    case _:
                        print("\nInvalid choice. Please try again.")

            case "7":
                print("\nExiting dashboard...")
                break

            case _:
                print("\nInvalid choice. Please try again.")

def goodbye():
    '''
    Goodbye():
    Prints goodbye message.
    Final call of the program.
    '''
    print("\n---------------------------------")
    print("--Thank you for using AFS Bank!--")
    print("---------------------------------")

#-----------------------helper functions------------------------#
def choose_account(customer: Customer, header: str = "Accounts available:") -> Account | None:
    if not customer.accounts:
        print("You have not created any accounts yet.")
        return None

    print(f"\n{header}")
    for account in customer.accounts:
        print(account)

    chosen_account_number = read_int("\nPlease enter your account number: ")
    for account in customer.accounts:
        if account.account_number == chosen_account_number:
            return account

    print("\nAccount number not found.")
    return None

def choose_branch(bank: Bank) -> Branch | None:
    print("\nBranches available:")
    for branch in bank.branches:
        print(f"{branch.branch_code}) {branch.location}")

    chosen_branch_code = read_int("\nPlease enter branch id: ")
    try:
        return bank.find_branch(chosen_branch_code)
    except NotFoundError:
        print("\nBranch not found.")
        return None

def read_amount(prompt: str) -> Decimal:
    while True:
        text = input(prompt)
        try:
            amount = Decimal(text)
        except InvalidOperation:
            print("Invalid input. Please try again.")
            continue

        quantized = amount.quantize(Decimal("0.01"))
        if quantized != amount:
            print("Amounts can only have up to 2 decimal places. Please try again.")
            continue

        return quantized

def read_int(prompt: str) -> int:
    while True:
        text = input(prompt)
        try:
            return int(text)
        except ValueError:
            print("Invalid input. Please try again.")


if __name__ == '__main__':
    main()