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
    -This specific exception should be raised when a user tries to withdraw more money
    than they have left in their Savings Account.
    '''

class NotFoundError(BankError):
    '''
    NotFoundError(BankError):
    -NotFoundError extends the BankError class.
    -This is a BankError but a specific kind, raised in a specific situation only.
    '''