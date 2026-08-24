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

    if login_res == "admin":
        admin_dashboard()
    elif login_res == "customer":
        customer_dashboard()
    else:
        print("Log in failed.")
        # moves to goodbye()

    goodbye()

def welcome():
    print("AFS Bank welcomes you!")

def goodbye():
    print("Thank you for using AFS Bank! Have a nice day!")

def login() -> str:
    print("Please enter your username and password.")

    #return "wrong login"
    #return "customer"
    return "admin"

def admin_dashboard():
    print("Hello admin.")

def customer_dashboard():
    print("Hello cust.")

if __name__ == '__main__':
    main()