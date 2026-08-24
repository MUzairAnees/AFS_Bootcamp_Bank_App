from bankapp.user import User, Customer, Admin, USERS

def main():
    '''
    Main():
    Acts as the entry point of the program.

    Purpose:
    1) Welcomes user -> welcome().

    2) Prompts for authorization -> login().
    2.a) If authorization returns a specific val(stored in check var)
    -> activates the related x_dashboard() -> x == admin or cust.

    3) Exits program -> goodbye().
    '''

    welcome()

    #login() -> contains login logic and stores results in var
    login_res = login()

    if isinstance(login_res, Admin):
        admin_dashboard()
    elif isinstance(login_res, Customer):
        customer_dashboard()
    else:
        print("Log in failed. Please try again.")
        # moves to goodbye()

    goodbye()

def welcome():
    print("AFS Bank welcomes you!")

def login() -> User | None:
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    #return the object
    for user in USERS:
        if user.username == username and user.password == password:
            return user

    #or return None
    return None

def admin_dashboard():
    print("Hello admin.")

def customer_dashboard():
    print("Hello cust.")

def goodbye():
    print("Thank you for using AFS Bank!")

if __name__ == '__main__':
    main()