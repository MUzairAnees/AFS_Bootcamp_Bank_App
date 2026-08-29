class BankError(Exception):
    '''
    BankError(Exception):
    -Whenever something goes wrong/any Exception occurs within the banking app, it is expressed as a BankError.
    '''

class InsufficientFundsError(BankError):
    '''
    InsufficientFundsError(BankError):
    -InsufficientFundsError extends the BankError class.
    -So this IS a BankError but a specific kind, raised in a specific situation only.
    -Raised when a withdrawal would take an account past what it is allowed to hold:
    below zero for a SavingsAccount, or past the overdraft limit for a CheckingAccount.
    '''

class NotFoundError(BankError):
    '''
    NotFoundError(BankError):
    -NotFoundError extends the BankError class.
    -This is a BankError but a specific kind, raised in a specific situation only.
    '''
