from ..CommonScripts import *

from colorama import Fore
from time import sleep
from tabulate import tabulate

def CustomerScreen(db, UserID):
    cursor = db.cursor()

    cursor.execute(f"SELECT Firstname FROM customers WHERE CustomerID = {UserID}")
    Name: str = cursor.fetchone()[0]

    print(Fore.GREEN + f"Welcome {Name}!")
    print("What would you like to do today?")
    print(Fore.WHITE + "*"*20)
    print(Fore.BLUE + "1. Check Account Balance")
    print(Fore.BLUE + "2. Open a new Account")
    print(Fore.BLUE + "3. View Account Transaction History")
    print(Fore.BLUE + "4. Transfer Funds")
    print(Fore.BLUE + "5. Apply for a Loan")
    print(Fore.BLUE + "6. View Active Loans")
    print(Fore.BLUE + "7. Apply for a bank card")
    print(Fore.BLUE + "8. View Bank Cards")
    print(Fore.BLUE + "9. Update Personal Information")
    print(Fore.BLUE + "10. Logout")

    choice_dict = {
        1: (lambda:CheckAccountBalance(db, UserID)),
        2: (lambda:OpenNewAccount(db, UserID)),
        3: (lambda:ViewAccountTransactionHistory(db, UserID)),
        4: (lambda:TransferFunds(db, UserID)),
        5: lambda:ApplyForLoan(db, UserID),
        6: (lambda:ViewActiveLoans(db, UserID)),
        7: (lambda:ApplyForCard(db, UserID)),
        8: (lambda:ViewActiveCards(db, UserID)),
        9: (lambda:UpdatePersonalInformation(db, UserID)),
        10: (lambda:ProgramExit())
    }

    choice = 0
    while choice not in choice_dict.keys():
        choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    choice_dict[choice]()

def CheckAccountBalance(db, UserID):
    cursor = db.cursor()

    try:
        cursor.execute("SELECT AccountNumber,AccountType FROM accounts WHERE AccountHolderID = %s", (UserID,))
        accounts = cursor.fetchall()
        if accounts:
            account_info = ["AccountNumber","AccountType"]
            print(tabulate(accounts, headers=account_info, tablefmt="pretty"))

            AccountNumber = input(Fore.GREEN + "Enter Account Number To View Balance For: " + Fore.YELLOW)

            cursor.execute("SELECT AccountBalance FROM accounts WHERE AccountNumber = %s AND AccountHolderID = %s", (AccountNumber, UserID))
            AccountBalance = cursor.fetchone()[0]

            print(Fore.GREEN + f"Account balance for account {AccountNumber}: " + Fore.CYAN + f"{AccountBalance}" + Fore.RESET)
            if AccountBalance < 0:
                print(Fore.RED + "Your account is in overdraft. Please deposit funds to avoid penalties." + Fore.RESET)


        else:
            print(Fore.RED + "No accounts found for the given User ID." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error viewing account details: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def ViewAccountTransactionHistory(db, UserID):
    cursor = db.cursor()

    try:
        # Fetch all accounts related to the user
        cursor.execute("SELECT AccountID,AccountNumber,AccountType,AccountBalance,AccountSecondaryHolderID FROM accounts WHERE AccountHolderID = %s", (UserID,))
        accounts = cursor.fetchall()
        if not accounts:
            print(Fore.RED + "No accounts found for the given User ID." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        account_info = ["AccountID", "AccountNumber","AccountType",
                        "AccountBalance", "AccountSecondaryHolderID"]
        print(Fore.GREEN + "Your accounts: " + Fore.YELLOW)
        print(tabulate(accounts, headers=account_info, tablefmt="pretty"))

        # Ask the user to select an account number
        AccountNumber = input(Fore.GREEN + "Enter the account number to view transactions: " + Fore.YELLOW)

        cursor.execute("SELECT AccountID FROM accounts WHERE AccountNumber = %s", (AccountNumber,))
        AccountID = cursor.fetchone()[0]

        # Fetch transactions for the selected account
        cursor.execute("SELECT * FROM transactionlogs WHERE DebitAccountID = %s OR CreditAccountID = %s ORDER BY TransactionDate DESC", (AccountID, AccountID))
        transactions = cursor.fetchall()
        if transactions:
            transaction_info = ["TransactionID", "DebitAccountID", "CreditAccountID", "TransactionType", "TransactionAmount", "TransactionDate", "TransactionDescription", "TransactionMedium"]
            print(Fore.GREEN + "Transaction history for account " + AccountNumber + ": " + Fore.YELLOW)
            print(tabulate(transactions, headers=transaction_info, tablefmt="pretty"))
        else:
            print(Fore.RED + "No transactions found for the selected account." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error viewing transaction history: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def TransferFunds(db, UserID):
    cursor = db.cursor()

    cursor.execute("SELECT AccountStatus FROM customers WHERE CustomerID = %s", (UserID,))
    status = cursor.fetchone()[0].lower()

    if status != 'active':
        print(Fore.RED + "Your account is not active. Please contact your nearest branch for assistance." + Fore.RESET)
        sleep(1.5)
        UserMenu(db, UserID)
        return

    try:
        from_account = input(Fore.GREEN + "Enter your account number: " + Fore.YELLOW)
        to_account = input(Fore.GREEN + "Enter the recipient's account number: " + Fore.YELLOW)
        amount = float(input(Fore.GREEN + "Enter the amount to transfer: " + Fore.YELLOW))

        cursor.execute("SELECT AccountBalance FROM accounts WHERE AccountNumber = %s AND AccountHolderID = %s", (from_account, UserID))
        from_account_balance = cursor.fetchone()
        if not from_account_balance:
            print(Fore.RED + "Invalid account number or insufficient funds." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        if from_account_balance[0] < amount:
            print(Fore.RED + "Insufficient funds." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        cursor.execute("SELECT AccountID FROM accounts WHERE AccountNumber = %s", (from_account,))
        from_account_id = cursor.fetchone()[0]

        cursor.execute("SELECT AccountID FROM accounts WHERE AccountNumber = %s", (to_account,))
        to_account_id = cursor.fetchone()[0]

        cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance - %s WHERE AccountNumber = %s AND AccountHolderID = %s", (amount, from_account, UserID))
        cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance + %s WHERE AccountNumber = %s", (amount, to_account))
        cursor.execute("""INSERT INTO transactionlogs (DebitAccountID, CreditAccountID, TransactionType, TransactionAmount, TransactionDescription, TransactionMedium) 
                          VALUES (%s, %s, %s, %s, %s, %s)""", (to_account_id, from_account_id, 'Transfer', amount, f'Transferred to account {to_account}', 'Netbanking'))
        db.commit()
        print(Fore.GREEN + "Funds transferred successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error transferring funds: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def UpdatePersonalInformation(db, UserID):
    cursor = db.cursor()

    try:
        field_to_update = input(Fore.GREEN + "Enter the field you want to update (e.g., ContactNumber, Email, Address): " + Fore.YELLOW).lower()
        new_value = input(Fore.GREEN + f"Enter new value for {field_to_update}: " + Fore.YELLOW)

        value_dict = {"first name": "Firstname","last name": "Lastname", "date of birth": "DateOfBirth",
                      "contact number": "ContactNumber", "email": "EmailID", "address": "PermanentResidence",
                      "password": "CustomerPassword"}
        
        if field_to_update in value_dict.keys():
            field_to_update = value_dict[field_to_update]
        else:
            print(Fore.RED + "Invalid field, Please approch your nearest branch to resolve the issue" + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        cursor.execute(f"UPDATE customers SET {field_to_update} = %s WHERE customerID = %s", (new_value, UserID))
        db.commit()
        print(Fore.GREEN + "Personal information updated successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error updating personal information: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def ApplyForLoan(db, UserID):
    cursor = db.cursor()

    try:
        cursor.execute("SELECT AccountStatus FROM customers WHERE CustomerID = %s", (UserID,))
        status = cursor.fetchone()[0].lower()

        if status != 'active':
            print(Fore.RED + "Your account is not active. Please contact your nearest branch for assistance." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        LoanType = input(Fore.GREEN + "Enter Loan Type (Home Loan, Gold Loan, Vehicle Loan, Mortgage Loan, Personal Loan, Education Loan): " + Fore.YELLOW)
        LoanAmmount = float(input(Fore.GREEN + "Enter Loan Amount: " + Fore.YELLOW))

        cursor.execute("INSERT INTO loans (CustomerID, LoanType, LoanAmmount, LoanStatus) VALUES (%s, %s, %s, %s)", (UserID, LoanType, LoanAmmount, 'Pending'))
        db.commit()
        print(Fore.GREEN + "Loan application submitted successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error applying for loan: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def ViewActiveLoans(db, UserID):
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM loans WHERE CustomerID = %s and LoanStatus = 'Approved'", (UserID,))
        loans = cursor.fetchall()
        if loans:
            loan_info = ["LoanID", "CustomerID", "LoanType", "LoanAmmount","LoanInterestRate",
                         "LoanStartDate","LoanMaturityDate", "LoanStatus","LoanUpdateDate","LoanAmmountDue"]
            
            print(Fore.GREEN + "Active loans: " + Fore.YELLOW)
            print(tabulate(loans, headers=loan_info, tablefmt="pretty"))
        else:
            print(Fore.RED + "No active loans found for the given User ID." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error viewing active loans: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def ApplyForCard(db, UserID):
    cursor = db.cursor()

    try:
        cursor.execute("SELECT AccountStatus FROM customers WHERE CustomerID = %s", (UserID,))
        status = cursor.fetchone()[0].lower()

        if status != 'active':
            print(Fore.RED + "Your account is not active. Please contact your nearest branch for assistance." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        # Fetch all accounts related to the user
        cursor.execute("SELECT AccountNumber,AccountType FROM accounts WHERE AccountHolderID = %s", (UserID,))
        accounts = cursor.fetchall()
        if not accounts:
            print(Fore.RED + "No accounts found for the given User ID." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        account_info = ["Account Number","Account Type"]
        print(Fore.GREEN + "Your accounts: " + Fore.YELLOW)
        print(tabulate(accounts, headers=account_info, tablefmt="pretty"))

        # Ask the user to select an account number
        AccountNumber = input(Fore.GREEN + "Enter the Account ID to apply for the card: " + Fore.YELLOW)

        CardType = input(Fore.GREEN + "Enter Card Type (Debit, Credit, Prepaid, ATM): " + Fore.YELLOW)
        CardIssuer = input(Fore.GREEN + "Enter Card Issuer (Visa, Mastercard, Rupay, American Express): " + Fore.YELLOW)

        cursor.execute("SELECT Firstname, Lastname FROM customers WHERE CustomerID = %s", (UserID,))
        Firstname, Lastname = cursor.fetchone()
        cursor.execute("SELECT AccountID FROM accounts WHERE AccountNumber = %s", (AccountNumber,))
        AccountID = cursor.fetchone()[0]

        cursor.execute("""INSERT INTO cards (CardHolderAccountID, CardType, CardStatus,
                       CardHolderFirstName, CardHolderLastName, CardIssuer) VALUES (%s, %s, %s, %s, %s, %s)""",
                       (AccountID, CardType, 'Pending', Firstname, Lastname, CardIssuer))
        db.commit()
        print(Fore.GREEN + "Card application submitted successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error applying for card: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def UserMenu(db, UserID):

    print(Fore.WHITE + "*"*20)
    print(Fore.MAGENTA + "What Would You Like To Do Next ?".center(20))
    print(Fore.BLUE + "1. Go Back To User Menu")
    print(Fore.BLUE + "2. Exit")
    print()

    choice = 0
    while choice not in (1, 2):
        choice = int(input(Fore.GREEN + "Enter Your Choice: " + Fore.YELLOW))

    if choice == 1: CustomerScreen(db, UserID)
    elif choice == 2: ProgramExit()

def OpenNewAccount(db, UserID):

    from random import randint
    cursor = db.cursor()

    try:
        cursor.execute("SELECT AccountStatus FROM customers WHERE CustomerID = %s", (UserID,))
        status = cursor.fetchone()[0].lower()

        if status != 'active':
            print(Fore.RED + "Your account is not active. Please contact your nearest branch for assistance." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return

        AccountNumber = str(randint(10000000, 99999999))
        AccountHolderID = UserID
        AccountType = input(Fore.GREEN + "Enter Account Type (Savings, Current, Salary, Recurring Deposit, Fixed Deposit): " + Fore.YELLOW)
        AccountSecondaryHolderID = input(Fore.GREEN + "Enter Account Secondary Holder ID (if any): " + Fore.YELLOW)
        AccountPassword = input(Fore.GREEN + "Enter Account Password: " + Fore.YELLOW)

        cursor.execute("""INSERT INTO accounts (
            AccountNumber, AccountHolderID, AccountType,
            AccountSecondaryHolderID, AccountPassword) 
            VALUES (%s, %s, %s, %s, %s)""",
            (AccountNumber, AccountHolderID, AccountType, AccountSecondaryHolderID, AccountPassword))
        db.commit()
        print(Fore.GREEN + "New account created successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error creating new account: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)

def ViewActiveCards(db, UserID):
    cursor = db.cursor()

    try:
        cursor.execute("SELECT CardNumber,CardIssuer,CardType,CardExpiaryDate,CardStatus FROM cards WHERE CardHolderAccountID = %s", (UserID,))
        cards = cursor.fetchall()

        if cards:
            card_info = ["CardNumber", "CardIssuer", "CardType", "CardExpiaryDate", "CardStatus"]
            print(Fore.GREEN + "Your cards: " + Fore.YELLOW)
            print(tabulate(cards, headers=card_info, tablefmt="pretty"))
        else:
            print(Fore.RED + "No cards found for the given User ID." + Fore.RESET)
            sleep(1.5)
            UserMenu(db, UserID)
            return
        
        ViewCVV = input(Fore.GREEN + "Would you like to View any card CVV code?(y/n): " + Fore.YELLOW).lower()
        if ViewCVV == 'y':
            CardNumber = input(Fore.GREEN + "Enter Card Number to view: " + Fore.YELLOW)

            CustomerPassword = input(Fore.GREEN + "Enter your password to view CVV: " + Fore.YELLOW)
            cursor.execute("SELECT CustomerPassword FROM customers WHERE CustomerID = %s", (UserID,))
            Password = cursor.fetchone()[0]

            if CustomerPassword != Password:
                print(Fore.RED + "Incorrect password. Please try again." + Fore.RESET)
                sleep(1.5)
                print(Fore.MAGENTA + "_"*20)
                ViewActiveCards(db, UserID)
                return

            cursor.execute("SELECT Card_CVV_Code FROM cards WHERE CardNumber = %s and CardHolderAccountID = %s", (CardNumber,UserID))
            CardCVV = cursor.fetchone()[0]
            print(Fore.GREEN + f"Card CVV Code for card numbered {CardNumber} is: " + Fore.CYAN + f"{CardCVV}" + Fore.RESET)

        for card in cards:
            if card[2] == 'Prepaid':
                print(Fore.MAGENTA + "_"*20)
                print(Fore.GREEN + "You appear to have a Prepaid card." + Fore.RESET)
                ViewBalance = input(Fore.GREEN + "Would you like to Check Prepaid Card Balance?(y/n): " + Fore.YELLOW).lower()
                if ViewBalance == 'y':
                    CardNumber = input(Fore.GREEN + "Enter Card Number to view: " + Fore.YELLOW)
                    cursor.execute("SELECT CardPrePaidAmt FROM cards WHERE CardNumber = %s and CardHolderAccountID = %s", (CardNumber,UserID))
                    CardPrePaidAmt = cursor.fetchone()[0]
                    print(Fore.GREEN + f"Card Prepaid Balance for card numbered {CardNumber} is: " + Fore.CYAN + f"{CardPrePaidAmt}" + Fore.RESET)
                break

    except Exception as e:
        print(Fore.RED + f"Error viewing cards: {e}" + Fore.RESET)

    sleep(1.5)
    UserMenu(db, UserID)