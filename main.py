from bankapp.bank import Bank, create_bank
from bankapp.user import User, Customer, Admin
from bankapp.account import *
from bankapp.exceptions import BankError, NotFoundError
from decimal import Decimal, InvalidOperation

def main():
    '''
    Main():
    Acts as the entry point of the program.

    Purpose:
    0) Creates a bank to work with.
    1) Welcomes user -> welcome().
    2) Prompts for authorization -> login().
    2.a) If authorization returns a specific val(stored in check var)
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
                       "3) Add a customer\n"
                       "4) Delete a customer\n"
                       "5) Update a customer\n"
                       "6) Exit\n"
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
                #Adds customer based on customerID -> only if customerID doesn't exist.
                customer_id = read_int("Please enter customer id: ")
                try:
                    bank.find_customer(customer_id)
                    print("Customer ID already exists.")
                except NotFoundError:
                    name = input("Please enter customer name: ")
                    email = input("Please enter customer email: ")
                    branch_id = read_int("Please enter customer branch id: ")
                    username = input("Please enter customer username: ")
                    password = input("Please enter customer password: ")

                    new_customer = Customer(customer_id, name, email, branch_id, username, password)
                    bank.add_user(new_customer)
                    print(f"\nCustomer {name}, {customer_id} added.")

            case "4":
                customer_to_delete_id = read_int("Please enter customer id: ")
                try:
                    bank.remove_customer(customer_to_delete_id)
                    print("\nCustomer deleted.")
                except NotFoundError:
                    print("Customer does not exist.")

            case "5":
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
                          "5) Password\n")
                    choice = input("Please enter your choice: ")

                    match choice:
                        case "1":
                            customer_to_update.name = input("Please enter new customer name: ")
                            print("\nCustomer updated.")
                        case "2":
                            customer_to_update.email = input("Please enter new customer email: ")
                            print("\nCustomer updated.")
                        case "3":
                            customer_to_update.branch_id = read_int("Please enter new customer branch id: ")
                            print("\nCustomer updated.")
                        case "4":
                            customer_to_update.username = input("Please enter new customer username: ")
                            print("\nCustomer updated.")
                        case "5":
                            customer_to_update.password = input("Please enter new customer password: ")
                            print("\nCustomer updated.")
                        case _:
                            print("Invalid choice. Please try again.")

            case "6":
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
                       "5) Exit\n"
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
                from_account = choose_account(customer)
                if from_account is not None:
                    to_account = choose_account(customer)

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
def choose_account(customer: Customer) -> Account | None:
    if not customer.accounts:
        print("You have not created any accounts yet.")
        return None

    print("\nAccounts available:")
    for account in customer.accounts:
        print(account)

    chosen_account_number = read_int("\nPlease enter your account number: ")
    for account in customer.accounts:
        if account.account_number == chosen_account_number:
            return account

    print("\nAccount number not found.")
    return None

def read_amount(prompt: str) -> Decimal:
    while True:
        text = input(prompt)
        try:
            return Decimal(text)
        except InvalidOperation:
            print("Invalid input. Please try again.")

def read_int(prompt: str) -> int:
    while True:
        text = input(prompt)
        try:
            return int(text)
        except ValueError:
            print("Invalid input. Please try again.")


if __name__ == '__main__':
    main()