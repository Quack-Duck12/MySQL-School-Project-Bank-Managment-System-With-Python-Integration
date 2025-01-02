# This file contains the AdminScreen function which is the main screen for the admin user.

# importing required modules
from ..CommonScripts import *

from tabulate import tabulate
from random import randint
from colorama import Fore
from time import sleep

# Function to display the Admin Main User Menu
def AdminScreen(db, ID):

    cursor = db.cursor()

    cursor.execute(f"SELECT EmployeeFirstName FROM Employees WHERE EmployeeID = {ID}")
    Name: str = cursor.fetchone()[0]

    print(Fore.BLUE + f"Welcome {Name}!")
    print("What would you like to do today?")
    print(Fore.WHITE + "*"*20)

    # Admin options related to customers
    print(Fore.MAGENTA + "Customer".center(20,'-'))
    print(Fore.BLUE + "1. Create a new customer")
    print(Fore.BLUE + "2. Update customer details")
    print(Fore.BLUE + "3. View customer details")
    print(Fore.LIGHTBLUE_EX + "4. Delete a customer")
    # Admin options related to accounts
    print(Fore.MAGENTA + "Account".center(20,'-'))
    print(Fore.BLUE + "5. Create a new account")
    print(Fore.BLUE + "6. Update account details")
    print(Fore.BLUE + "7. View account details")
    print(Fore.LIGHTBLUE_EX + "8. Delete an account")
    # Admin options related to transactions
    print(Fore.MAGENTA + "Transaction".center(20,'-'))
    print(Fore.BLUE + "9. Record a new transaction")
    print(Fore.BLUE + "10. View transaction history")
    print(Fore.LIGHTBLUE_EX + "11. Reverse a transaction")
    # Admin options related to employees
    print(Fore.MAGENTA + "Employee".center(20,'-'))
    print(Fore.BLUE + "12. Create a new employee account")
    print(Fore.BLUE + "13. Update employee details")
    print(Fore.BLUE + "14. View employee details")
    print(Fore.LIGHTBLUE_EX + "15. Delete an employee account")
    # Admin options related to cards
    print(Fore.MAGENTA + "Cards".center(20,'-'))
    print(Fore.BLUE + "16. Issue a new card")
    print(Fore.BLUE + "17. Add Aditional Funds to a Prepaid Card")
    print(Fore.BLUE + "18. View card details")
    print(Fore.LIGHTBLUE_EX + "19. Block a card")
    # Admin options related to loans
    print(Fore.MAGENTA + "Loans".center(20,'-'))
    print(Fore.BLUE + "20. Issue a new loan")
    print(Fore.BLUE + "21. Update loan ammount due")
    print(Fore.BLUE + "22. View loan details")
    print(Fore.LIGHTBLUE_EX + "23. Default a loan")
    # Admin options related to branches
    print(Fore.MAGENTA + "Branches".center(20,'-'))
    print(Fore.BLUE + "24. Add a new branch")
    print(Fore.BLUE + "25. Update branch employee count")
    print(Fore.BLUE + "26. View branch details")
    # Admin options related to logs
    print(Fore.MAGENTA + "Logs".center(20,'-'))
    print(Fore.BLUE + "27. Check logs")
    print(Fore.BLUE + "28. Save Logs to a external .Json File")
    print(Fore.LIGHTRED_EX + "29. Clear Logs")
    # Other options
    print()

    print(Fore.MAGENTA + "30. Exit")
    #Takeing user input
    print()
    choice: int = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    # Dictionary to map the choice to the function
    choiceDict = {
        1: CreateCustomer, 2: UpdateCustomer, 3: ViewCustomer, 4: DeleteCustomer, 5: CreateAccount,
        6: UpdateAccount, 7: ViewAccount, 8: DeleteAccount,
        9: RecordTransaction, 10: ViewTransaction, 11: ReverseTransaction,
        12: CreateEmployee, 13: UpdateEmployee, 14: ViewEmployee, 15: DeleteEmployee,
        16: IssueCard, 17: CardExtendPrePaidAmt, 18: ViewCard, 19: BlockCard,
        20: IssueLoan, 21: UpdateLoan, 22: ViewLoan, 23: DefaultLoan,
        24: AddBranch, 25: UpdateBranch, 26: ViewBranch,
        30: ProgramExit, 27: CheckLogs, 29: ClearLogs, 28: SaveLogs
    }
    # Calling the function based on the choice
    if choice <= 29: choiceDict[choice](db, ID)
    else: choiceDict[choice]()

# Function to create a new customer
def CreateCustomer(db, ID):
    cursor = db.cursor()
    # Taking the input from the user
    FirstName = input(Fore.GREEN + "Enter First Name: " + Fore.YELLOW)
    LastName = input(Fore.GREEN + "Enter Last Name: " + Fore.YELLOW)
    DateOfBirth = input(Fore.GREEN + "Enter Date of Birth (YYYY-MM-DD): " + Fore.YELLOW)
    ContactNumber = input(Fore.GREEN + "Enter Contact Number: " + Fore.YELLOW)
    EmailID = input(Fore.GREEN + "Enter Email ID: " + Fore.YELLOW)
    PermanentResidence = input(Fore.GREEN + "Enter Permanent Residence: " + Fore.YELLOW)
    RegisteredIDType = input(Fore.GREEN + "Enter Registered ID Type(AadharCard,Passport,PANCard,Driving License,Other): " + Fore.YELLOW)
    IDNumber = input(Fore.GREEN + "Enter ID Number: " + Fore.YELLOW)
    IDExpiryDate = input(Fore.GREEN + "Enter ID Expiry Date (YYYY-MM-DD): " + Fore.YELLOW)
    CustomerPassword = input(Fore.GREEN + "Enter Customer Password: " + Fore.YELLOW)

    # Inserting the data into the database
    try:
        cursor.execute(f"""INSERT INTO customers (
            Firstname, Lastname, DateOfBirth, ContactNumber, EmailID, 
            PermanentResidence, RegisteredIDType, IDNumber, IDExpiryDate, 
            CustomerPassword) 
            VALUES(
            '{FirstName}', '{LastName}', '{DateOfBirth}', '{ContactNumber}', '{EmailID}', 
            '{PermanentResidence}', '{RegisteredIDType}', '{IDNumber}', '{IDExpiryDate}', 
            '{CustomerPassword}' 
        );""")
        db.commit()
        print(Fore.GREEN + "Customer created successfully." + Fore.RESET)
        log_event(db, ID, f"Customer with Name {FirstName} {LastName} created", True)
    except Exception as e:
        print(Fore.RED + f"Error creating customer: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to create customer named {FirstName} {LastName}", False)

    sleep(1.5)
    AdminMenu(db, ID)

# Function to update customer details
def UpdateCustomer(db, ID):
    cursor = db.cursor()
    # Taking the input from the user
    CustomerID = input(Fore.GREEN + "Enter Customer ID to update: " + Fore.YELLOW)

    # Fetch current customer details
    cursor.execute(f"SELECT * FROM customers WHERE CustomerID = {CustomerID};")
    customer = cursor.fetchone()
    if not customer:
        print(Fore.RED + "Customer not found." + Fore.RESET)
        sleep(1.5)
        AdminMenu(db, ID)
    # Displaying the current customer details
    field_to_update = input(Fore.GREEN + "Enter the field you want to update (e.g., Firstname, Lastname, etc.): " + Fore.YELLOW)
    new_value = input(Fore.GREEN + f"Enter new value for {field_to_update}: " + Fore.YELLOW)
    # Updating the customer details
    try:
        cursor.execute(f"UPDATE customers SET {field_to_update} = {new_value} WHERE CustomerID = {CustomerID};")
        db.commit()
        print(Fore.GREEN + "Customer updated successfully." + Fore.RESET)
        log_event(db, ID, f"Updated customer {customer[1]} {customer[2]}", True)
    except Exception as e:
        print(Fore.RED + f"Error updating customer: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to update customer {customer[1]} {customer[2]}", False)

    sleep(1.5)
    AdminMenu(db, ID)

# Function to view customer details
def ViewCustomer(db, ID):
    cursor = db.cursor()
    # Taking the input from the user
    print(Fore.GREEN + "How would you like to search for the customer?" + Fore.YELLOW)
    print(Fore.BLUE + "1. Search by ID")
    print(Fore.BLUE + "2. Search by Detail")
    print(Fore.BLUE + "3. View All Customers")
    choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    customer_info = ["CustomerID", "Firstname", "Lastname", "DateOfBirth", "ContactNumber",
                                 "EmailID", "PermanentResidence", "RegisteredIDType", "IDNumber",
                                 "IDExpiryDate", "AccountStatus", "CreatedAt", "UpdatedAt", "CustomerPassword"]

    # Displaying the customer details based on the choice
    if choice == 1:
        CustomerID = input(Fore.GREEN + "Enter Customer ID: " + Fore.YELLOW)

        try:
            # Displaying the customer details based on the ID
            cursor.execute("SELECT * FROM customers WHERE CustomerID = %s", (CustomerID,))
            Customer = cursor.fetchone()
            if Customer:
                print(Fore.GREEN + "Customer details: " + Fore.YELLOW)

                print(tabulate([Customer], headers=customer_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed customer {Customer[1]} {Customer[2]}", True)
            else:
                print(Fore.RED + "Customer not found." + Fore.RESET)
                log_event(db, ID, f"Failed to view customer with ID {CustomerID}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing customer: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing customer with ID {CustomerID}", False)

    elif choice == 2:
        # Taking the input from the user
        field_to_filter = input(Fore.GREEN + "Enter the field you want to filter by (e.g., Firstname, Lastname, etc.): " + Fore.YELLOW)
        filter_value = input(Fore.GREEN + f"Enter value for {field_to_filter}: " + Fore.YELLOW)

        try:
            # Displaying the customer details based on the filter
            query = f"SELECT * FROM customers WHERE {field_to_filter} = %s"
            cursor.execute(query, (filter_value,))
            customers = cursor.fetchall()
            if customers:
                print(Fore.GREEN + "Customer details: " + Fore.YELLOW)

                print(tabulate(customers, headers=customer_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed customers with {field_to_filter} = {filter_value}", True)
            else:
                print(Fore.RED + "No customers found with the given info." + Fore.RESET)
                log_event(db, ID, f"Failed to view customers with {field_to_filter} = {filter_value}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing customers: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing customers with {field_to_filter} = {filter_value}", False)

    elif choice == 3:
        # Displaying all the customer details
        try:
            cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()
            if customers:
                print(Fore.GREEN + "All customer details: " + Fore.YELLOW)

                print(tabulate(customers, headers=customer_info, tablefmt="pretty"))
                log_event(db, ID, "Viewed all customers", True)
            else:
                print(Fore.RED + "No customers found." + Fore.RESET)
                log_event(db, ID, "Failed to view all customers", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing all customers: {e}" + Fore.RESET)
            log_event(db, ID, "Error viewing all customers", False)

    else:
        print(Fore.RED + "Invalid choice." + Fore.RESET)
        log_event(db, ID, "Invalid choice in ViewCustomer", False)

    sleep(1.5)
    AdminMenu(db, ID)

# Function to delete a customer
def DeleteCustomer(db, ID):
    cursor = db.cursor()
    # Taking the input from the user
    CustomerID = input(Fore.GREEN + "Enter Customer ID to delete: " + Fore.YELLOW)

    # Fetch current customer details
    cursor.execute("SELECT * FROM customers WHERE CustomerID = %s", (CustomerID,))
    customer = cursor.fetchone()
    if not customer:
        print(Fore.RED + "Customer not found." + Fore.RESET)
        log_event(db, ID, f"Failed to delete customer with ID {CustomerID}", False)
        return
    # Displaying the current customer details
    delete_query = f"DELETE FROM customers WHERE CustomerID = {CustomerID};"
    print(Fore.RED + "WARNING: You are about to delete the following customer:" + Fore.RESET)
    customer_info = ["CustomerID", "Firstname", "Lastname", "DateOfBirth", "ContactNumber",
                     "EmailID", "PermanentResidence", "RegisteredIDType", "IDNumber",
                     "IDExpiryDate", "AccountStatus", "CreatedAt", "UpdatedAt", "CustomerPassword"]

    print(tabulate([customer], headers=customer_info, tablefmt="pretty"))
    print(Fore.RED + f"To confirm deletion, type the following query exactly as shown:" + Fore.RESET)
    print(Fore.YELLOW + delete_query + Fore.RESET)
    # Asking for Confirmoation before deleting the customer
    confirmation = input(Fore.GREEN + "Enter the query to confirm deletion: " + Fore.YELLOW)
    # Deleting the customer
    if confirmation == delete_query:
        try:
            cursor.execute(delete_query)
            db.commit()
            print(Fore.GREEN + "Customer deleted successfully." + Fore.RESET)
            log_event(db, ID, f"Deleted customer {customer[1]} {customer[2]}", True)
        except Exception as e:
            print(Fore.RED + f"Error deleting customer: {e}" + Fore.RESET)
            log_event(db, ID, f"Failed to delete customer {customer[1]} {customer[2]}", False)
    else:# If the query does not match
        print(Fore.RED + "Deletion cancelled. The entered query did not match." + Fore.RESET)
        log_event(db, ID, f"Deletion cancelled for customer {customer[1]} {customer[2]}", False)

    sleep(1.5)
    AdminMenu(db, ID)
# Function to create a new account
def CreateAccount(db, ID):

    cursor = db.cursor()
    # Taking the input from the user
    AccountNumber = str(randint(10000000, 99999999))
    AccountHolderID = input(Fore.GREEN + "Enter Account Holder ID: " + Fore.YELLOW)
    AccountType = input(Fore.GREEN + "Enter Account Type (Savings, Current, Salary, Recurring Deposit, Fixed Deposit): " + Fore.YELLOW)
    #AccountBalance = input(Fore.GREEN + "Enter Account Balance: " + Fore.YELLOW)
    #AccountStatus = input(Fore.GREEN + "Enter Account Status (Active, Inactive, Closed, Frozen): " + Fore.YELLOW)
    AccountSecondaryHolderID = input(Fore.GREEN + "Enter Account Secondary Holder ID (if any): " + Fore.YELLOW)
    AccountPassword = input(Fore.GREEN + "Enter Account Password: " + Fore.YELLOW)

    if not AccountSecondaryHolderID:
        AccountSecondaryHolderID = None
    # Inserting the data into the database
    try:
        cursor.execute("""INSERT INTO accounts (
            AccountNumber, AccountHolderID, AccountType,
            AccountSecondaryHolderID, AccountPassword) 
            VALUES (%s, %s, %s, %s, %s)""",
            (AccountNumber, AccountHolderID, AccountType, AccountSecondaryHolderID, AccountPassword))
        db.commit()
        print(Fore.GREEN + f"Account created successfully numbered {AccountNumber}." + Fore.RESET)
        log_event(db, ID, f"Account {AccountNumber} created for holder ID {AccountHolderID}", True)
    except Exception as e:
        print(Fore.RED + f"Error creating account: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to create account {AccountNumber} for holder ID {AccountHolderID}", False)

    sleep(1.5)
    AdminMenu(db, ID)
# Function to update account details
def UpdateAccount(db, ID):
    cursor = db.cursor()

    AccountID = input(Fore.GREEN + "Enter Account ID to update: " + Fore.YELLOW)

    # Fetch current account details
    cursor.execute("SELECT * FROM accounts WHERE AccountID = %s", (AccountID,))
    account = cursor.fetchone()
    if not account:
        print(Fore.RED + "Account not found." + Fore.RESET)
        log_event(db, ID, f"Failed to update account with ID {AccountID}", False)
        sleep(1.5)
        AdminMenu(db, ID)
    # Displaying the current account details
    field_to_update = input(Fore.GREEN + "Enter the field you want to update (e.g., AccountNumber, AccountHolderID, etc.): " + Fore.YELLOW)
    new_value = input(Fore.GREEN + f"Enter new value for {field_to_update}: " + Fore.YELLOW)
    # Updating the account details
    try:
        cursor.execute(f"UPDATE accounts SET {field_to_update} = %s WHERE AccountID = %s", (new_value, AccountID))
        db.commit()
        print(Fore.GREEN + "Account updated successfully." + Fore.RESET)
        log_event(db, ID, f"Updated account {AccountID} - set {field_to_update} to {new_value}", True)
    except Exception as e:
        print(Fore.RED + f"Error updating account: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to update account {AccountID} - set {field_to_update} to {new_value}", False)

    sleep(1.5)
    AdminMenu(db, ID)
# Function to view account details
def ViewAccount(db, ID):
    cursor = db.cursor()
    # Taking the input from the user
    print(Fore.GREEN + "How would you like to search for the account?" + Fore.YELLOW)
    print(Fore.BLUE + "1. Search by Account ID")
    print(Fore.BLUE + "2. Search by Detail")
    print(Fore.BLUE + "3. View All Accounts")
    choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    account_info = ["AccountID", "AccountNumber", "AccountHolderID", "AccountType", "AccountBalance",
                                "AccountOpened", "AccountStatus", "AccountSecondaryHolderID", "AccountPassword"]
    # Displaying the account details based on the choice
    if choice == 1:
        AccountID = input(Fore.GREEN + "Enter Account ID: " + Fore.YELLOW)

        try:# Displaying the account details based on the ID
            cursor.execute("SELECT * FROM accounts WHERE AccountID = %s", (AccountID,))
            account = cursor.fetchone()
            if account:
                print(Fore.GREEN + "Account details: " + Fore.YELLOW)

                print(tabulate([account], headers=account_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed account {account[1]}", True)
            else:
                print(Fore.RED + "Account not found." + Fore.RESET)
                log_event(db, ID, f"Failed to view account with ID {AccountID}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing account: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing account with ID {AccountID}", False)

    elif choice == 2:
        # Taking the input from the user
        field_to_filter = input(Fore.GREEN + "Enter the field you want to filter by (e.g., AccountNumber, AccountHolderID, etc.): " + Fore.YELLOW)
        filter_value = input(Fore.GREEN + f"Enter value for {field_to_filter}: " + Fore.YELLOW)

        try:# Displaying the account details based on the filter
            query = f"SELECT * FROM accounts WHERE {field_to_filter} = %s"
            cursor.execute(query, (filter_value,))
            accounts = cursor.fetchall()
            if accounts:
                print(Fore.GREEN + "Account details: " + Fore.YELLOW)

                print(tabulate(accounts, headers=account_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed accounts with {field_to_filter} = {filter_value}", True)
            else:
                print(Fore.RED + "No accounts found with the given info." + Fore.RESET)
                log_event(db, ID, f"Failed to view accounts with {field_to_filter} = {filter_value}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing accounts: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing accounts with {field_to_filter} = {filter_value}", False)

    elif choice == 3:
        try:# Displaying all the account details
            cursor.execute("SELECT * FROM accounts")
            accounts = cursor.fetchall()
            if accounts:
                print(Fore.GREEN + "All account details: " + Fore.YELLOW)

                print(tabulate(accounts, headers=account_info, tablefmt="pretty"))
                log_event(db, ID, "Viewed all accounts", True)
            else:
                print(Fore.RED + "No accounts found." + Fore.RESET)
                log_event(db, ID, "Failed to view all accounts", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing all accounts: {e}" + Fore.RESET)
            log_event(db, ID, "Error viewing all accounts", False)

    else:
        print(Fore.RED + "Invalid choice." + Fore.RESET)
        log_event(db, ID, "Invalid choice in ViewAccount", False)

    sleep(1.5)
    AdminMenu(db, ID)

# Function to delete an account
def DeleteAccount(db, ID):
    cursor = db.cursor()

    AccountID = input(Fore.GREEN + "Enter Account ID to delete: " + Fore.YELLOW)

    # Fetch current account details
    cursor.execute("SELECT * FROM accounts WHERE AccountID = %s", (AccountID,))
    account = cursor.fetchone()
    if not account:
        print(Fore.RED + "Account not found." + Fore.RESET)
        log_event(db, ID, f"Failed to delete account with ID {AccountID}", False)
        return
    # Displaying the current account details
    delete_query = f"DELETE FROM accounts WHERE AccountID = {AccountID};"
    print(Fore.RED + "WARNING: You are about to delete the following account:" + Fore.RESET)
    account_info = ["AccountID", "AccountNumber", "AccountHolderID", "AccountType", "AccountBalance",
                    "AccountOpened", "AccountStatus", "AccountSecondaryHolderID", "AccountPassword"]
    # Displaying the account details
    print(tabulate([account], headers=account_info, tablefmt="pretty"))
    # Asking for Confirmoation before deleting the account
    print(Fore.RED + f"To confirm deletion, type the following query exactly as shown:" + Fore.RESET)
    print(Fore.YELLOW + delete_query + Fore.RESET)

    confirmation = input(Fore.GREEN + "Enter the query to confirm deletion: " + Fore.YELLOW)
    # Deleting the account
    if confirmation == delete_query:
        try:
            cursor.execute(delete_query)
            db.commit()
            print(Fore.GREEN + "Account deleted successfully." + Fore.RESET)
            log_event(db, ID, f"Deleted account {account[1]}", True)
        except Exception as e:
            print(Fore.RED + f"Error deleting account: {e}" + Fore.RESET)
            log_event(db, ID, f"Failed to delete account {account[1]}", False)
    else:
        print(Fore.RED + "Deletion cancelled. The entered query did not match." + Fore.RESET)
        log_event(db, ID, f"Deletion cancelled for account {account[1]}", False)

    sleep(1.5)
    AdminMenu(db, ID)
# Function to Manually record a transaction
def RecordTransaction(db, ID):
    cursor = db.cursor()

    TransactionType = input(Fore.GREEN + "Enter Transaction Type (Deposit, Withdrawal, Transfer): " + Fore.YELLOW)
    # Taking the input from the user
    if TransactionType == "Deposit":
        DebitAccountID = input(Fore.GREEN + "Enter Debit Account ID: " + Fore.YELLOW)
        CreditAccountID = 0
    elif TransactionType == "Withdrawal":
        DebitAccountID = 0
        CreditAccountID = input(Fore.GREEN + "Enter Credit Account ID: " + Fore.YELLOW)
    elif TransactionType == "Transfer":
        DebitAccountID = input(Fore.GREEN + "Enter Debit Account ID: " + Fore.YELLOW)
        CreditAccountID = input(Fore.GREEN + "Enter Credit Account ID: " + Fore.YELLOW)
    else:
        print(Fore.RED + "Invalid transaction type." + Fore.RESET)
        log_event(db, ID, f"Failed to record transaction due to invalid transaction type {TransactionType}", False)
        sleep(1.5)
        AdminMenu(db, ID)

    # To Check if the provided account IDs exist in the accounts table
    if DebitAccountID != 0:
        cursor.execute("SELECT COUNT(*) FROM accounts WHERE AccountID = %s", (DebitAccountID,))
        if cursor.fetchone()[0] == 0:
            print(Fore.RED + "Debit Account ID does not exist." + Fore.RESET)
            log_event(db, ID, f"Failed to record transaction due to non-existent Debit Account ID {DebitAccountID}", False)
            sleep(1.5)
            AdminMenu(db, ID)
    # To Check if the provided account IDs exist in the accounts table
    if CreditAccountID != 0:
        cursor.execute("SELECT COUNT(*) FROM accounts WHERE AccountID = %s", (CreditAccountID,))
        if cursor.fetchone()[0] == 0:
            print(Fore.RED + "Credit Account ID does not exist." + Fore.RESET)
            log_event(db, ID, f"Failed to record transaction due to non-existent Credit Account ID {CreditAccountID}", False)
            sleep(1.5)
            AdminMenu(db, ID)
            return
    # Taking the input from the user
    TransactionAmount = float(input(Fore.GREEN + "Enter Transaction Amount: " + Fore.YELLOW))
    TransactionDescription = input(Fore.GREEN + "Enter Transaction Description: " + Fore.YELLOW)
    TransactionMedium = input(Fore.GREEN + "Enter Transaction Medium (Cash, Cheque, Netbanking, Other): " + Fore.YELLOW)

    try:    # Inserting the data into the database
        cursor.execute("""INSERT INTO transactionlogs (
            DebitAccountID, CreditAccountID, TransactionType, TransactionAmount, TransactionDescription, TransactionMedium) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (DebitAccountID, CreditAccountID, TransactionType, TransactionAmount, TransactionDescription, TransactionMedium))
        
        if TransactionType == "Deposit":
            cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance + %s WHERE AccountID = %s", (TransactionAmount, DebitAccountID))
        elif TransactionType == "Withdrawal":
            cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance - %s WHERE AccountID = %s", (TransactionAmount, CreditAccountID))
        elif TransactionType == "Transfer":
            cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance - %s WHERE AccountID = %s", (TransactionAmount, DebitAccountID))
            cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance + %s WHERE AccountID = %s", (TransactionAmount, CreditAccountID))
        
        db.commit()
        print(Fore.GREEN + "Transaction recorded successfully." + Fore.RESET)
        log_event(db, ID, f"Recorded {TransactionType} transaction from account {DebitAccountID} to account {CreditAccountID}", True)
    except Exception as e:
        print(Fore.RED + f"Error recording transaction: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to record {TransactionType} transaction from account {DebitAccountID} to account {CreditAccountID}", False)

    sleep(1.5)
    AdminMenu(db, ID)
# Function to view a transaction
def ViewTransaction(db, ID):
    cursor = db.cursor()
    # Taking the input from the user
    print(Fore.GREEN + "How would you like to view the transactions?" + Fore.YELLOW)
    print(Fore.BLUE + "1. View all transactions of an inputted AccountID")
    print(Fore.BLUE + "2. View all transactions of a certain date")
    print(Fore.BLUE + "3. View all Deposit, Withdrawal, Transfer transactions")
    print(Fore.BLUE + "4. View all transactions")
    choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    if choice == 1:
        AccountID = input(Fore.GREEN + "Enter Account ID: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM transactionlogs WHERE DebitAccountID = %s OR CreditAccountID = %s", (AccountID, AccountID))
            transactions = cursor.fetchall()
            if transactions:
                print(Fore.GREEN + "Transaction details: " + Fore.YELLOW)

                transaction_info = ["TransactionID", "DebitAccountID", "CreditAccountID", "TransactionType", "TransactionAmount",
                                    "TransactionDate", "TransactionDescription", "TransactionMedium"]

                print(tabulate(transactions, headers=transaction_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed transactions for account {AccountID}", True)
            else:
                print(Fore.RED + "No transactions found for the given Account ID." + Fore.RESET)
                log_event(db, ID, f"Failed to view transactions for account {AccountID}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing transactions: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing transactions for account {AccountID}", False)

    elif choice == 2:
        TransactionDate = input(Fore.GREEN + "Enter Transaction Date (YYYY-MM-DD): " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM transactionlogs WHERE DATE(TransactionDate) = %s", (TransactionDate,))
            transactions = cursor.fetchall()
            if transactions:
                print(Fore.GREEN + "Transaction details: " + Fore.YELLOW)

                transaction_info = ["TransactionID", "DebitAccountID", "CreditAccountID", "TransactionType", "TransactionAmount",
                                    "TransactionDate", "TransactionDescription", "TransactionMedium"]

                print(tabulate(transactions, headers=transaction_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed transactions for date {TransactionDate}", True)
            else:
                print(Fore.RED + "No transactions found for the given date." + Fore.RESET)
                log_event(db, ID, f"Failed to view transactions for date {TransactionDate}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing transactions: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing transactions for date {TransactionDate}", False)

    elif choice == 3:
        TransactionType = input(Fore.GREEN + "Enter Transaction Type (Deposit, Withdrawal, Transfer): " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM transactionlogs WHERE TransactionType = %s", (TransactionType,))
            transactions = cursor.fetchall()
            if transactions:
                print(Fore.GREEN + "Transaction details: " + Fore.YELLOW)

                transaction_info = ["TransactionID", "DebitAccountID", "CreditAccountID", "TransactionType", "TransactionAmount",
                                    "TransactionDate", "TransactionDescription", "TransactionMedium"]

                print(tabulate(transactions, headers=transaction_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed {TransactionType} transactions", True)
            else:
                print(Fore.RED + f"No {TransactionType} transactions found." + Fore.RESET)
                log_event(db, ID, f"Failed to view {TransactionType} transactions", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing transactions: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing {TransactionType} transactions", False)

    elif choice == 4:
        sort_option = input(Fore.GREEN + "Sort by Transaction Date? (y/n): " + Fore.YELLOW).lower()
        if sort_option == 'y':
            order = input(Fore.GREEN + "Enter sort order (asc/desc): " + Fore.YELLOW).lower()
            if order not in ['asc', 'desc']:
                print(Fore.RED + "Invalid sort order." + Fore.RESET)
                log_event(db, ID, "Invalid sort order in ViewTransaction", False)
                sleep(1.5)
                AdminMenu(db, ID)
                return
            query = f"SELECT * FROM transactionlogs ORDER BY TransactionDate {order.upper()}"
        else:
            query = "SELECT * FROM transactionlogs"

        try:
            cursor.execute(query)
            transactions = cursor.fetchall()
            if transactions:
                print(Fore.GREEN + "All transaction details: " + Fore.YELLOW)

                transaction_info = ["TransactionID", "DebitAccountID", "CreditAccountID", "TransactionType", "TransactionAmount",
                                    "TransactionDate", "TransactionDescription", "TransactionMedium"]

                print(tabulate(transactions, headers=transaction_info, tablefmt="pretty"))
                log_event(db, ID, "Viewed all transactions", True)
            else:
                print(Fore.RED + "No transactions found." + Fore.RESET)
                log_event(db, ID, "Failed to view all transactions", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing all transactions: {e}" + Fore.RESET)
            log_event(db, ID, "Error viewing all transactions", False)

    else:
        print(Fore.RED + "Invalid choice." + Fore.RESET)
        log_event(db, ID, "Invalid choice in ViewTransaction", False)

    sleep(1.5)
    AdminMenu(db, ID)

def ReverseTransaction(db, ID):
    cursor = db.cursor()

    TransactionID = input(Fore.GREEN + "Enter Transaction ID to reverse: " + Fore.YELLOW)

    # Fetch the original transaction details
    cursor.execute("SELECT * FROM transactionlogs WHERE TransactionID = %s", (TransactionID,))
    transaction = cursor.fetchone()
    if not transaction:
        print(Fore.RED + "Transaction not found." + Fore.RESET)
        log_event(db, ID, f"Failed to reverse transaction with ID {TransactionID}", False)
        sleep(1.5)
        AdminMenu(db, ID)

    DebitAccountID = transaction[2]
    CreditAccountID = transaction[1]
    TransactionAmount = transaction[4]
    TransactionDescription = f"Reversal of Transaction {TransactionID}"
    TransactionMedium = "Netbanking"

    try:
        cursor.execute("""INSERT INTO transactionlogs (
            DebitAccountID, CreditAccountID, TransactionType, TransactionAmount, TransactionDescription, TransactionMedium) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (DebitAccountID, CreditAccountID, 'Transfer', TransactionAmount, TransactionDescription, TransactionMedium))
        
        cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance - %s WHERE AccountID = %s", (TransactionAmount, CreditAccountID))
        cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance + %s WHERE AccountID = %s", (TransactionAmount, DebitAccountID))
        
        db.commit()
        print(Fore.GREEN + "Transaction reversed successfully." + Fore.RESET)
        log_event(db, ID, f"Reversed transaction {TransactionID}", True)
    except Exception as e:
        print(Fore.RED + f"Error reversing transaction: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to reverse transaction {TransactionID}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def CreateEmployee(db, ID):
    cursor = db.cursor()

    EmployeeFirstName = input(Fore.GREEN + "Enter Employee First Name: " + Fore.YELLOW)
    EmployeeLastName = input(Fore.GREEN + "Enter Employee Last Name: " + Fore.YELLOW)
    EmployeeDOB = input(Fore.GREEN + "Enter Employee Date of Birth (YYYY-MM-DD): " + Fore.YELLOW)
    EmployeeContactNumber = input(Fore.GREEN + "Enter Employee Contact Number: " + Fore.YELLOW)
    EmployeePersonalEmailID = input(Fore.GREEN + "Enter Employee Personal Email ID: " + Fore.YELLOW)
    EmployeeCompanyAssignedEmailID = input(Fore.GREEN + "Enter Employee Company Assigned Email ID: " + Fore.YELLOW)
    EmployeeResidenceAddress = input(Fore.GREEN + "Enter Employee Residence Address: " + Fore.YELLOW)
    EmployeeBranchID = input(Fore.GREEN + "Enter Employee Branch ID: " + Fore.YELLOW)
    EmployeePositionShortCode = input(Fore.GREEN + "Enter Employee Position Short Code: " + Fore.YELLOW)
    EmployeeRegisteredIDType = input(Fore.GREEN + "Enter Employee Registered ID Type (AadhaarCard, PANCard, DrivingLicense, Other): " + Fore.YELLOW)
    EmployeeIDNumber = input(Fore.GREEN + "Enter Employee ID Number: " + Fore.YELLOW)
    EmployeeIDExpiryDate = input(Fore.GREEN + "Enter Employee ID Expiry Date (YYYY-MM-DD): " + Fore.YELLOW)
    EmployeeGender = input(Fore.GREEN + "Enter Employee Gender (Male, Female, Other): " + Fore.YELLOW)
    EmployeeMaritalStatus = input(Fore.GREEN + "Enter Employee Marital Status (Single, Married, Divorced, Widowed): " + Fore.YELLOW)
    EmployeeBankAccountID = input(Fore.GREEN + "Enter Employee Bank Account ID: " + Fore.YELLOW)
    EmployeePrivilege = input(Fore.GREEN + "Enter Employee Privilege (Top_Level_Admin, Admin, None): " + Fore.YELLOW)
    EmployeePassword = input(Fore.GREEN + "Enter Employee Password: " + Fore.YELLOW)

    EmployeePayRaisePercentage = 0
    EmployeeEmploymentStatus = "Employed"

    cursor.execute(f"SELECT EmployeePrivilege FROM employees WHERE EmployeeID = {ID};")
    Current_Privilege = cursor.fetchone()[0]

    print(Current_Privilege)

    if Current_Privilege != "Top-Level Admin" and EmployeePrivilege == "Top_Level_Admin":
        print(Fore.LIGHTRED_EX + "You do not have the privilege to create a Top-Level Admin." + Fore.RESET)
        print(Fore.LIGHTRED_EX + "Creating employee with Admim Privilege Only." + Fore.RESET)
        EmployeePrivilege = "Admin"

    try:
        cursor.execute(f"""INSERT INTO employees (
            EmployeeFirstName, EmployeeLastName, EmployeeDOB, EmployeeContactNumber, EmployeePersonalEmailID, 
            EmployeeCompanyAssignedEmailID, EmployeeResidenceAddress, EmployeeBranchID, EmployeePositionShortCode, 
            EmployeePayRaisePercentage, EmployeeRegisteredIDType, EmployeeIDNumber, EmployeeIDExpiryDate, 
            EmployeeGender, EmployeeMaritalStatus, EmployeeEmploymentStatus, EmployeeBankAccountID, 
            EmployeePrivilege, EmployeePassword) 
            VALUES ('{EmployeeFirstName}', '{EmployeeLastName}', '{EmployeeDOB}', '{EmployeeContactNumber}', '{EmployeePersonalEmailID}',
            '{EmployeeCompanyAssignedEmailID}', '{EmployeeResidenceAddress}', {EmployeeBranchID}, {EmployeePositionShortCode},
            {EmployeePayRaisePercentage}, '{EmployeeRegisteredIDType}', '{EmployeeIDNumber}', '{EmployeeIDExpiryDate}',
            '{EmployeeGender}', '{EmployeeMaritalStatus}', '{EmployeeEmploymentStatus}', {EmployeeBankAccountID},
            '{EmployeePrivilege}', '{EmployeePassword}');""")
        db.commit()
        print(Fore.GREEN + "Employee created successfully." + Fore.RESET)
        log_event(db, ID, f"Created employee {EmployeeFirstName} {EmployeeLastName}", True)
    except Exception as e:
        print(Fore.RED + f"Error creating employee: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to create employee {EmployeeFirstName} {EmployeeLastName}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def UpdateEmployee(db, ID):
    cursor = db.cursor()

    EmployeeID = input(Fore.GREEN + "Enter Employee ID to update: " + Fore.YELLOW)

    # Fetch current employee details
    cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (EmployeeID,))
    employee = cursor.fetchone()
    if not employee:
        print(Fore.RED + "Employee not found." + Fore.RESET)
        log_event(db, ID, f"Failed to update employee with ID {EmployeeID}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    field_to_update = input(Fore.GREEN + "Enter the field you want to update (e.g., EmployeeFirstName, EmployeeLastName, etc.): " + Fore.YELLOW)
    
    if field_to_update == "EmployeeID":
        print(Fore.RED + "Updating EmployeeID is not allowed due to foreign key constraints." + Fore.RESET)
        log_event(db, ID, f"Attempted to update EmployeeID for employee {EmployeeID}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return
    
    if field_to_update == "EmployeePassword":
        cursor.execute("SELECT EmployeePrivilege FROM employees WHERE EmployeeID = %s", (ID,))
        Privilege = cursor.fetchone()[0]
        if Privilege != "Top-Level Admin":
            print(Fore.RED + "You do not have the privilege to update Employee Password." + Fore.RESET)
            log_event(db, ID, f"Failed to update Employee Password for employee {EmployeeID}", False)
            sleep(1.5)
            AdminMenu(db, ID)
            return


    new_value = input(Fore.GREEN + f"Enter new value for {field_to_update}: " + Fore.YELLOW)

    try:
        cursor.execute(f"UPDATE employees SET {field_to_update} = %s WHERE EmployeeID = %s", (new_value, EmployeeID))
        db.commit()
        print(Fore.GREEN + "Employee updated successfully." + Fore.RESET)
        log_event(db, ID, f"Updated employee {EmployeeID} - set {field_to_update} to {new_value}", True)
    except Exception as e:
        print(Fore.RED + f"Error updating employee: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to update employee {EmployeeID} - set {field_to_update} to {new_value}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def ViewEmployee(db, ID):
    cursor = db.cursor()

    # Check the privilege of the current user
    cursor.execute("SELECT EmployeePrivilege FROM employees WHERE EmployeeID = %s", (ID,))
    user_privilege = cursor.fetchone()[0]

    print(Fore.GREEN + "How would you like to view the employees?" + Fore.YELLOW)
    print(Fore.BLUE + "1. View all employees of an inputted EmployeeID")
    print(Fore.BLUE + "2. View all employees of a certain joining date")
    print(Fore.BLUE + "3. View all employees by privilege")
    print(Fore.BLUE + "4. View all employees by EmployeeBranchID")
    print(Fore.BLUE + "5. View all employees by EmployeePositionShortCode")
    print(Fore.BLUE + "6. Search employees by keyword")
    print(Fore.BLUE + "7. View all employees")
    choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    employee_info = ["EmployeeID", "EmployeeFirstName", "EmployeeLastName", "EmployeeDOB", "EmployeeContactNumber",
                     "EmployeePersonalEmailID", "EmployeeCompanyAssignedEmailID", "EmployeeResidenceAddress", 
                     "EmployeeBranchID", "EmployeePositionShortCode", "EmployeePayRaisePercentage", 
                     "EmployeeRegisteredIDType", "EmployeeIDNumber", "EmployeeIDExpiryDate", "EmployeeJoinDate", 
                     "EmployeeGender", "EmployeeMaritalStatus", "EmployeeEmploymentStatus", "EmployeeBankAccountID", 
                     "EmployeePrivilege", "EmployeePassword"]

    if choice == 1:
        EmployeeID = input(Fore.GREEN + "Enter Employee ID: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (EmployeeID,))
            employees = cursor.fetchall()
            if employees:
                if user_privilege != "Top_Level_Admin":
                    employees = [list(employee) for employee in employees]  # Convert tuples to lists
                    for employee in employees:
                        employee[-1] = "********"  # Censor the password
                print(Fore.GREEN + "Employee details: " + Fore.YELLOW)
                print(tabulate(employees, headers=employee_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed employee {EmployeeID}", True)
            else:
                print(Fore.RED + "No employees found for the given Employee ID." + Fore.RESET)
                log_event(db, ID, f"Failed to view employee for Employee ID {EmployeeID}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing employee: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing employee for Employee ID {EmployeeID}", False)

    elif choice == 2:
        EmployeeJoinDate = input(Fore.GREEN + "Enter Employee Join Date (YYYY-MM-DD): " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM employees WHERE EmployeeJoinDate = %s", (EmployeeJoinDate,))
            employees = cursor.fetchall()
            if employees:
                if user_privilege != "Top_Level_Admin":
                    employees = [list(employee) for employee in employees]  # Convert tuples to lists
                    for employee in employees:
                        employee[-1] = "********"  # Censor the password
                print(Fore.GREEN + "Employee details: " + Fore.YELLOW)
                print(tabulate(employees, headers=employee_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed employees with join date {EmployeeJoinDate}", True)
            else:
                print(Fore.RED + "No employees found for the given join date." + Fore.RESET)
                log_event(db, ID, f"Failed to view employees for join date {EmployeeJoinDate}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing employees: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing employees for join date {EmployeeJoinDate}", False)

    elif choice == 3:
        EmployeePrivilege = input(Fore.GREEN + "Enter Employee Privilege: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM employees WHERE EmployeePrivilege = %s", (EmployeePrivilege,))
            employees = cursor.fetchall()
            if employees:
                if user_privilege != "Top_Level_Admin":
                    employees = [list(employee) for employee in employees]  # Convert tuples to lists
                    for employee in employees:
                        employee[-1] = "********"  # Censor the password
                print(Fore.GREEN + "Employee details: " + Fore.YELLOW)
                print(tabulate(employees, headers=employee_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed employees with privilege {EmployeePrivilege}", True)
            else:
                print(Fore.RED + "No employees found for the given privilege." + Fore.RESET)
                log_event(db, ID, f"Failed to view employees for privilege {EmployeePrivilege}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing employees: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing employees for privilege {EmployeePrivilege}", False)

    elif choice == 4:
        EmployeeBranchID = input(Fore.GREEN + "Enter Employee Branch ID: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM employees WHERE EmployeeBranchID = %s", (EmployeeBranchID,))
            employees = cursor.fetchall()
            if employees:
                if user_privilege != "Top_Level_Admin":
                    employees = [list(employee) for employee in employees]  # Convert tuples to lists
                    for employee in employees:
                        employee[-1] = "********"  # Censor the password
                print(Fore.GREEN + "Employee details: " + Fore.YELLOW)
                print(tabulate(employees, headers=employee_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed employees with branch ID {EmployeeBranchID}", True)
            else:
                print(Fore.RED + "No employees found for the given branch ID." + Fore.RESET)
                log_event(db, ID, f"Failed to view employees for branch ID {EmployeeBranchID}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing employees: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing employees for branch ID {EmployeeBranchID}", False)

    elif choice == 5:
        EmployeePositionShortCode = input(Fore.GREEN + "Enter Employee Position Short Code: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM employees WHERE EmployeePositionShortCode = %s", (EmployeePositionShortCode,))
            employees = cursor.fetchall()
            if employees:
                if user_privilege != "Top_Level_Admin":
                    employees = [list(employee) for employee in employees]  # Convert tuples to lists
                    for employee in employees:
                        employee[-1] = "********"  # Censor the password
                print(Fore.GREEN + "Employee details: " + Fore.YELLOW)
                print(tabulate(employees, headers=employee_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed employees with position short code {EmployeePositionShortCode}", True)
            else:
                print(Fore.RED + "No employees found for the given position short code." + Fore.RESET)
                log_event(db, ID, f"Failed to view employees for position short code {EmployeePositionShortCode}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing employees: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing employees for position short code {EmployeePositionShortCode}", False)

    elif choice == 6:
        field_to_filter = input(Fore.GREEN + "Enter the field you want to filter by (e.g., EmployeeFirstName, EmployeeContactNumber, etc.): " + Fore.YELLOW)
        filter_value = input(Fore.GREEN + f"Enter value for {field_to_filter}: " + Fore.YELLOW)

        try:
            query = f"SELECT * FROM employees WHERE {field_to_filter} = %s"
            cursor.execute(query, (filter_value,))
            employees = cursor.fetchall()
            if employees:
                if user_privilege != "Top_Level_Admin":
                    employees = [list(employee) for employee in employees]  # Convert tuples to lists
                    for employee in employees:
                        employee[-1] = "********"  # Censor the password
                print(Fore.GREEN + "Employee details: " + Fore.YELLOW)
                print(tabulate(employees, headers=employee_info, tablefmt="pretty"))
                log_event(db, ID, f"Searched employees by keyword {field_to_filter} = {filter_value}", True)
            else:
                print(Fore.RED + "No employees found for the given keyword." + Fore.RESET)
                log_event(db, ID, f"Failed to search employees by keyword {field_to_filter} = {filter_value}", False)
        except Exception as e:
            print(Fore.RED + f"Error searching employees: {e}" + Fore.RESET)
            log_event(db, ID, f"Error searching employees by keyword {field_to_filter} = {filter_value}", False)

    elif choice == 7:
        try:
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            if employees:
                if user_privilege != "Top_Level_Admin":
                    employees = [list(employee) for employee in employees]  # Convert tuples to lists
                    for employee in employees:
                        employee[-1] = "********"  # Censor the password
                print(Fore.GREEN + "All employee details: " + Fore.YELLOW)
                print(tabulate(employees, headers=employee_info, tablefmt="pretty"))
                log_event(db, ID, "Viewed all employees", True)
            else:
                print(Fore.RED + "No employees found." + Fore.RESET)
                log_event(db, ID, "Failed to view all employees", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing all employees: {e}" + Fore.RESET)
            log_event(db, ID, "Error viewing all employees", False)

    else:
        print(Fore.RED + "Invalid choice." + Fore.RESET)
        log_event(db, ID, "Invalid choice in ViewEmployee", False)

    sleep(1.5)
    AdminMenu(db, ID)

def DeleteEmployee(db, ID):
    cursor = db.cursor()

    EmployeeID = input(Fore.GREEN + "Enter Employee ID to delete: " + Fore.YELLOW)

    # Fetch current employee details
    cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (EmployeeID,))
    employee = cursor.fetchone()
    if not employee:
        print(Fore.RED + "Employee not found." + Fore.RESET)
        log_event(db, ID, f"Failed to delete employee with ID {EmployeeID}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        

    print(Fore.RED + f"To confirm deletion, type the following query exactly as shown:" + Fore.YELLOW)
    confirmation_query = f"DELETE FROM employees WHERE EmployeeID = {EmployeeID}"
    print(Fore.YELLOW + f"Type the following query to confirm deletion: {confirmation_query}")
    confirmation = input(Fore.GREEN + "Enter the query to confirm deletion: " + Fore.YELLOW)

    if confirmation != confirmation_query:
        print(Fore.RED + "Deletion cancelled. The entered query did not match." + Fore.RESET)
        log_event(db, ID, f"Deletion cancelled for employee {EmployeeID}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        

    try:
        cursor.execute("DELETE FROM employees WHERE EmployeeID = %s", (EmployeeID,))
        db.commit()
        print(Fore.GREEN + "Employee deleted successfully." + Fore.RESET)
        log_event(db, ID, f"Deleted employee {EmployeeID}", True)
    except Exception as e:
        print(Fore.RED + f"Error deleting employee: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to delete employee {EmployeeID}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def IssueCard(db, ID):
    cursor = db.cursor()

    CardHolderAccountID = input(Fore.GREEN + "Enter Card Holder Account ID: " + Fore.YELLOW)
    CardIssuer = input(Fore.GREEN + "Enter Card Issuer (Visa, Mastercard, Rupay, American Express): " + Fore.YELLOW)
    CardType = input(Fore.GREEN + "Enter Card Type (Debit, Credit, Prepaid, ATM): " + Fore.YELLOW)
    CardHolderFirstName = input(Fore.GREEN + "Enter Card Holder First Name: " + Fore.YELLOW)
    CardHolderLastName = input(Fore.GREEN + "Enter Card Holder Last Name: " + Fore.YELLOW)
    CardExpiaryDate = input(Fore.GREEN + "Enter Card Expiry Date (YYYY-MM-DD): " + Fore.YELLOW)
    CardAnnualFees = input(Fore.GREEN + "Enter Card Annual Fees (default is 200): " + Fore.YELLOW) or 200

    CardNumber = ''.join([str(randint(0, 9)) for _ in range(16)])
    Card_CVV_Code = ''.join([str(randint(0, 9)) for _ in range(3)])

    if CardType == 'Prepaid':
        CardPrePaidAmt = input(Fore.GREEN + "Enter Card Prepaid Amount: " + Fore.YELLOW)
    else: CardPrePaidAmt = None

    try:
        cursor.execute("""INSERT INTO cards (
            CardNumber, CardHolderAccountID, CardIssuer, CardType, CardHolderFirstName, 
            CardHolderLastName, CardExpiaryDate, Card_CVV_Code, CardAnnualFees, CardPrePaidAmt) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (CardNumber, CardHolderAccountID, CardIssuer, CardType, CardHolderFirstName, 
            CardHolderLastName, CardExpiaryDate, Card_CVV_Code, CardAnnualFees, CardPrePaidAmt))
        db.commit()
        print(Fore.GREEN + "Card issued successfully." + Fore.RESET)
        log_event(db, ID, f"Issued card {CardNumber} for account {CardHolderAccountID}", True)
    except Exception as e:
        print(Fore.RED + f"Error issuing card: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to issue card for account {CardHolderAccountID}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def CardExtendPrePaidAmt(db, ID):
    cursor = db.cursor()

    CardNumber = input(Fore.GREEN + "Enter Card Number: " + Fore.YELLOW)

    # Check if the card exists and is a prepaid card
    cursor.execute("SELECT CardHolderAccountID, CardType, CardPrePaidAmt, CardStatus FROM cards WHERE CardNumber = %s", (CardNumber,))
    card = cursor.fetchone()
    if not card:
        print(Fore.RED + "Card not found." + Fore.RESET)
        log_event(db, ID, f"Failed to extend prepaid amount for non-existent card {CardNumber}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    CardHolderAccountID, CardType, CardPrePaidAmt, CardStatus = card
    if CardType != 'Prepaid':
        print(Fore.RED + "This card is not a prepaid card." + Fore.RESET)
        log_event(db, ID, f"Failed to extend prepaid amount for non-prepaid card {CardNumber}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return
    
    if CardStatus != 'Active':
        print(Fore.RED + "This card is not active." + Fore.RESET)
        log_event(db, ID, f"Failed to extend prepaid amount for inactive card {CardNumber}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    ExtendAmount = float(input(Fore.GREEN + "Enter amount to extend (up to 2 decimal places): " + Fore.YELLOW))
    PaymentMedium = input(Fore.GREEN + "Enter payment medium (Cash, Transfer): " + Fore.YELLOW).lower()

    if PaymentMedium == "transfer":
        # Subtract the amount from the CardHolderAccountID balance and add to the card's prepaid balance
        try:
            cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance - %s WHERE AccountID = %s", (ExtendAmount, CardHolderAccountID))
            cursor.execute("UPDATE cards SET CardPrePaidAmt = CardPrePaidAmt + %s WHERE CardNumber = %s", (ExtendAmount, CardNumber))
            cursor.execute("""INSERT INTO transactionlogs (
                DebitAccountID, CreditAccountID, TransactionType, TransactionAmount, TransactionDescription, TransactionMedium) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (-1, CardHolderAccountID, 'Transfer', ExtendAmount, f'Funds Transferred To Card Number {CardNumber}', 'Netbanking'))
            db.commit()
            print(Fore.GREEN + "Prepaid amount extended successfully via transfer." + Fore.RESET)
            log_event(db, ID, f"Extended prepaid amount {ExtendAmount} via transfer to card {CardNumber}", True)
        except Exception as e:
            print(Fore.RED + f"Error extending prepaid amount: {e}" + Fore.RESET)
            log_event(db, ID, f"Failed to extend prepaid amount via transfer to card {CardNumber}", False)

    elif PaymentMedium == "cash":
        # Add the amount to the card's prepaid balance and record a deposit transaction for the '-1' account ID
        try:
            cursor.execute("UPDATE accounts SET AccountBalance = AccountBalance + %s WHERE AccountID = %s", (ExtendAmount, CardHolderAccountID))
            cursor.execute("UPDATE cards SET CardPrePaidAmt = CardPrePaidAmt + %s WHERE CardNumber = %s", (ExtendAmount, CardNumber))
            cursor.execute("""INSERT INTO transactionlogs (
                DebitAccountID, CreditAccountID, TransactionType, TransactionAmount, TransactionDescription, TransactionMedium) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (-1, CardHolderAccountID, 'Deposit', ExtendAmount, f'Funds Deposited To Card Number {CardNumber}', 'Cash'))
            db.commit()
            print(Fore.GREEN + "Prepaid amount extended successfully via cash." + Fore.RESET)
            log_event(db, ID, f"Extended prepaid amount {ExtendAmount} via cash to card {CardNumber}", True)
        except Exception as e:
            print(Fore.RED + f"Error extending prepaid amount: {e}" + Fore.RESET)
            log_event(db, ID, f"Failed to extend prepaid amount via cash to card {CardNumber}", False)

    else:
        print(Fore.RED + "Invalid payment medium." + Fore.RESET)
        log_event(db, ID, f"Failed to extend prepaid amount due to invalid payment medium {PaymentMedium}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def ViewCard(db, ID):
    cursor = db.cursor()

    print(Fore.GREEN + "How would you like to view the cards?" + Fore.YELLOW)
    print(Fore.BLUE + "1. View card by Card Number")
    print(Fore.BLUE + "2. View card by Card ID")
    print(Fore.BLUE + "3. View cards by Card Type")
    print(Fore.BLUE + "4. View all cards")
    choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    card_info = ["CardID", "CardNumber", "CardHolderAccountID", "CardIssuer", "CardType", "CardHolderFirstName", 
                 "CardHolderLastName", "CardIssueDate", "CardExpiaryDate", "Card_CVV_Code", "CardStatus", "CardAnnualFees", "CardPrePaidAmt"]

    if choice == 1:
        CardNumber = input(Fore.GREEN + "Enter Card Number: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM cards WHERE CardNumber = %s", (CardNumber,))
            cards = cursor.fetchall()
            if cards:
                print(Fore.GREEN + "Card details: " + Fore.YELLOW)
                print(tabulate(cards, headers=card_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed card {CardNumber}", True)
            else:
                print(Fore.RED + "No cards found for the given Card Number." + Fore.RESET)
                log_event(db, ID, f"Failed to view card for Card Number {CardNumber}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing card: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing card for Card Number {CardNumber}", False)

    elif choice == 2:
        CardID = input(Fore.GREEN + "Enter Card ID: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM cards WHERE CardID = %s", (CardID,))
            cards = cursor.fetchall()
            if cards:
                print(Fore.GREEN + "Card details: " + Fore.YELLOW)
                print(tabulate(cards, headers=card_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed card {CardID}", True)
            else:
                print(Fore.RED + "No cards found for the given Card ID." + Fore.RESET)
                log_event(db, ID, f"Failed to view card for Card ID {CardID}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing card: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing card for Card ID {CardID}", False)

    elif choice == 3:
        CardType = input(Fore.GREEN + "Enter Card Type (Debit, Credit, Prepaid, ATM): " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM cards WHERE CardType = %s", (CardType,))
            cards = cursor.fetchall()
            if cards:
                print(Fore.GREEN + "Card details: " + Fore.YELLOW)
                print(tabulate(cards, headers=card_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed cards of type {CardType}", True)
            else:
                print(Fore.RED + f"No cards found for the given Card Type." + Fore.RESET)
                log_event(db, ID, f"Failed to view cards for Card Type {CardType}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing cards: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing cards for Card Type {CardType}", False)

    elif choice == 4:
        sort_option = input(Fore.GREEN + "Sort by Card Issue Date? (y/n): " + Fore.YELLOW).lower()
        if sort_option == 'y':
            order = input(Fore.GREEN + "Enter sort order (asc/desc): " + Fore.YELLOW).lower()
            if order not in ['asc', 'desc']:
                print(Fore.RED + "Invalid sort order." + Fore.RESET)
                log_event(db, ID, "Invalid sort order in ViewCard", False)
                sleep(1.5)
                AdminMenu(db, ID)
                return
            query = f"SELECT * FROM cards ORDER BY CardIssueDate {order.upper()}"
        else:
            query = "SELECT * FROM cards"

        try:
            cursor.execute(query)
            cards = cursor.fetchall()
            if cards:
                print(Fore.GREEN + "All card details: " + Fore.YELLOW)
                print(tabulate(cards, headers=card_info, tablefmt="pretty"))
                log_event(db, ID, "Viewed all cards", True)
            else:
                print(Fore.RED + "No cards found." + Fore.RESET)
                log_event(db, ID, "Failed to view all cards", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing all cards: {e}" + Fore.RESET)
            log_event(db, ID, "Error viewing all cards", False)

    else:
        print(Fore.RED + "Invalid choice." + Fore.RESET)
        log_event(db, ID, "Invalid choice in ViewCard", False)

    sleep(1.5)
    AdminMenu(db, ID)

def BlockCard(db, ID):
    cursor = db.cursor()

    CardNumber = input(Fore.GREEN + "Enter Card Number to block: " + Fore.YELLOW)

    # Check if the card exists
    cursor.execute("SELECT CardStatus FROM cards WHERE CardNumber = %s", (CardNumber,))
    card = cursor.fetchone()
    if not card:
        print(Fore.RED + "Card not found." + Fore.RESET)
        log_event(db, ID, f"Failed to block non-existent card {CardNumber}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    CardStatus = card[0]
    if CardStatus == "Blocked":
        print(Fore.RED + "Card is already blocked." + Fore.RESET)
        log_event(db, ID, f"Attempted to block already blocked card {CardNumber}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    try:
        cursor.execute("UPDATE cards SET CardStatus = 'Blocked' WHERE CardNumber = %s", (CardNumber,))
        db.commit()
        print(Fore.GREEN + "Card blocked successfully." + Fore.RESET)
        log_event(db, ID, f"Blocked card {CardNumber}", True)
    except Exception as e:
        print(Fore.RED + f"Error blocking card: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to block card {CardNumber}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def IssueLoan(db, ID):
    cursor = db.cursor()

    CustomerID = input(Fore.GREEN + "Enter Customer ID: " + Fore.YELLOW)
    LoanType = input(Fore.GREEN + "Enter Loan Type (Home Loan, Gold Loan, Vehicle Loan, Mortgage Loan, Personal Loan, Education Loan): " + Fore.YELLOW)
    LoanAmmount = float(input(Fore.GREEN + "Enter Loan Amount: " + Fore.YELLOW))
    LoanInterestRate = float(input(Fore.GREEN + "Enter Loan Interest Rate (default is 8.00): " + Fore.YELLOW) or 8.00)
    LoanMaturityDate = input(Fore.GREEN + "Enter Loan Maturity Date (YYYY-MM-DD): " + Fore.YELLOW)
    LoanStatus = "Approved"

    LoanAmmountDue = LoanAmmount 

    try:
        cursor.execute("""INSERT INTO loans (
            CustomerID, LoanType, LoanAmmount, LoanAmmountDue, LoanInterestRate, LoanMaturityDate, LoanStatus) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (CustomerID, LoanType, LoanAmmount, LoanAmmountDue, LoanInterestRate, LoanMaturityDate, LoanStatus))
        db.commit()
        print(Fore.GREEN + "Loan issued successfully." + Fore.RESET)
        log_event(db, ID, f"Issued loan of amount {LoanAmmount} to customer {CustomerID}", True)
    except Exception as e:
        print(Fore.RED + f"Error issuing loan: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to issue loan to customer {CustomerID}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def UpdateLoan(db, ID):
    from datetime import datetime

    cursor = db.cursor()

    LoanID = input(Fore.GREEN + "Enter Loan ID to update amount due: " + Fore.YELLOW)

    # Fetch current loan details
    cursor.execute("SELECT LoanUpdateDate, LoanAmmount, LoanInterestRate, LoanAmmountDue, LoanStatus FROM loans WHERE LoanID = %s", (LoanID,))
    loan = cursor.fetchone()
    if not loan:
        print(Fore.RED + "Loan not found." + Fore.RESET)
        log_event(db, ID, f"Failed to update loan with ID {LoanID}", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    LoanUpdateDate, LoanAmmount, LoanInterestRate, LoanAmmountDue, LoanStatus = loan
    today = datetime.now()

    if LoanStatus != "Approved":
        print(Fore.RED + "This loan is not approved." + Fore.RESET)
        log_event(db, ID, f"Failed to update loan {LoanID} - not approved", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    # Calculate the year difference
    year_difference = today.year - LoanUpdateDate.year - ((today.month, today.day) < (LoanUpdateDate.month, LoanUpdateDate.day))

    # Calculate the accrued interest
    Accrued_interest = LoanAmmount * (LoanInterestRate / 100) * year_difference

    # Update the amount due
    LoanAmmountDue += Accrued_interest

    try:
        cursor.execute("UPDATE loans SET LoanAmmountDue = %s, LoanUpdateDate = %s WHERE LoanID = %s", (LoanAmmountDue, today, LoanID))
        db.commit()
        print(Fore.GREEN + "Loan updated successfully." + Fore.RESET)
        log_event(db, ID, f"Updated loan {LoanID} - set LoanAmmountDue to {LoanAmmountDue}", True)
    except Exception as e:
        print(Fore.RED + f"Error updating loan: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to update loan {LoanID} - set LoanAmmountDue to {LoanAmmountDue}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def ViewLoan(db, ID):
    cursor = db.cursor()

    print(Fore.GREEN + "How would you like to view the loans?" + Fore.YELLOW)
    print(Fore.BLUE + "1. View issued loans by Loan Type")
    print(Fore.BLUE + "2. View issued loans by Loan Maturity Date")
    print(Fore.BLUE + "3. View all loans by their Status")
    print(Fore.BLUE + "4. View all loans")
    choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    loan_info = ["LoanID", "CustomerID", "LoanType", "LoanAmmount","LoanInterestRate",
                "LoanStartDate","LoanMaturityDate", "LoanStatus","LoanUpdateDate","LoanAmmountDue"]

    if choice == 1:
        LoanType = input(Fore.GREEN + "Enter Loan Type (Home Loan, Gold Loan, Vehicle Loan, Mortgage Loan, Personal Loan, Education Loan): " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM loans WHERE LoanType = %s", (LoanType,))
            loans = cursor.fetchall()
            if loans:
                print(Fore.GREEN + "Loan details: " + Fore.YELLOW)
                print(tabulate(loans, headers=loan_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed loans of type {LoanType}", True)
            else:
                print(Fore.RED + "No loans found for the given Loan Type." + Fore.RESET)
                log_event(db, ID, f"Failed to view loans for Loan Type {LoanType}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing loans: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing loans for Loan Type {LoanType}", False)

    elif choice == 2:
        LoanMaturityDate = input(Fore.GREEN + "Enter Loan Maturity Date (YYYY-MM-DD): " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM loans WHERE LoanMaturityDate = %s", (LoanMaturityDate,))
            loans = cursor.fetchall()
            if loans:
                print(Fore.GREEN + "Loan details: " + Fore.YELLOW)
                print(tabulate(loans, headers=loan_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed loans with maturity date {LoanMaturityDate}", True)
            else:
                print(Fore.RED + "No loans found for the given Loan Maturity Date." + Fore.RESET)
                log_event(db, ID, f"Failed to view loans for Loan Maturity Date {LoanMaturityDate}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing loans: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing loans for Loan Maturity Date {LoanMaturityDate}", False)

    elif choice == 3:
        LoanStatus = input(Fore.GREEN + "Enter Loan Status (Approved, Rejected, Pending, Paid, Defaulted): " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM loans WHERE LoanStatus = %s", (LoanStatus,))
            loans = cursor.fetchall()
            if loans:
                print(Fore.GREEN + "Loan details: " + Fore.YELLOW)
                print(tabulate(loans, headers=loan_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed loans with status {LoanStatus}", True)
            else:
                print(Fore.RED + "No loans found for the given Loan Status." + Fore.RESET)
                log_event(db, ID, f"Failed to view loans for Loan Status {LoanStatus}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing loans: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing loans for Loan Status {LoanStatus}", False)

    elif choice == 4:
        sort_option = input(Fore.GREEN + "Sort by Loan Start Date? (y/n): " + Fore.YELLOW).lower()
        if sort_option == 'y':
            order = input(Fore.GREEN + "Enter sort order (asc/desc): " + Fore.YELLOW).lower()
            if order not in ['asc', 'desc']:
                print(Fore.RED + "Invalid sort order." + Fore.RESET)
                log_event(db, ID, "Invalid sort order in ViewLoan", False)
                sleep(1.5)
                AdminMenu(db, ID)
                return
            query = f"SELECT * FROM loans ORDER BY LoanStartDate {order.upper()}"
        else:
            query = "SELECT * FROM loans"

        try:
            cursor.execute(query)
            loans = cursor.fetchall()
            if loans:
                print(Fore.GREEN + "All loan details: " + Fore.YELLOW)
                print(tabulate(loans, headers=loan_info, tablefmt="pretty"))
                log_event(db, ID, "Viewed all loans", True)
            else:
                print(Fore.RED + "No loans found." + Fore.RESET)
                log_event(db, ID, "Failed to view all loans", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing all loans: {e}" + Fore.RESET)
            log_event(db, ID, "Error viewing all loans", False)

    else:
        print(Fore.RED + "Invalid choice." + Fore.RESET)
        log_event(db, ID, "Invalid choice in ViewLoan", False)

    sleep(1.5)
    AdminMenu(db, ID)

def DefaultLoan(db, ID):
    cursor = db.cursor()

    LoanID = input(Fore.GREEN + "Enter Loan ID to mark as default: " + Fore.YELLOW)

    # Check if the loan exists
    cursor.execute("SELECT LoanStatus FROM loans WHERE LoanID = %s", (LoanID,))
    loan = cursor.fetchone()
    if not loan:
        print(Fore.RED + "Loan not found." + Fore.RESET)
        log_event(db, ID, f"Failed to mark non-existent loan {LoanID} as default", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    LoanStatus = loan[0]
    if LoanStatus == "Defaulted":
        print(Fore.RED + "Loan is already marked as defaulted." + Fore.RESET)
        log_event(db, ID, f"Attempted to mark already defaulted loan {LoanID} as default", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    try:
        cursor.execute("UPDATE loans SET LoanStatus = 'Defaulted' WHERE LoanID = %s", (LoanID,))
        db.commit()
        print(Fore.GREEN + "Loan marked as defaulted successfully." + Fore.RESET)
        log_event(db, ID, f"Marked loan {LoanID} as defaulted", True)
    except Exception as e:
        print(Fore.RED + f"Error marking loan as defaulted: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to mark loan {LoanID} as defaulted", False)

    sleep(1.5)
    AdminMenu(db, ID)

def AddBranch(db, ID):
    cursor = db.cursor()

    BranchName = input(Fore.GREEN + "Enter Branch Name: " + Fore.YELLOW)
    BranchAddress = input(Fore.GREEN + "Enter Branch Address: " + Fore.YELLOW)
    BranchContactNumber = input(Fore.GREEN + "Enter Branch Contact Number: " + Fore.YELLOW)
    BranchEmployeeCount = int(input(Fore.GREEN + "Enter Branch Employee Count: " + Fore.YELLOW))

    try:
        cursor.execute("""INSERT INTO branches (
            BranchName, BranchAddress, BranchContactNumber, BranchEmployeeCount) 
            VALUES (%s, %s, %s, %s)""",
            (BranchName, BranchAddress, BranchContactNumber, BranchEmployeeCount))
        db.commit()
        print(Fore.GREEN + "Branch added successfully." + Fore.RESET)
        log_event(db, ID, f"Added branch {BranchName}", True)
    except Exception as e:
        print(Fore.RED + f"Error adding branch: {e}" + Fore.RESET)
        log_event(db, ID, f"Failed to add branch {BranchName}", False)

    sleep(1.5)
    AdminMenu(db, ID)

def UpdateBranch(db, ID):
    cursor = db.cursor()

    try:
        # Fetch all branch IDs
        cursor.execute("SELECT BranchId FROM branches")
        branches = cursor.fetchall()

        for branch in branches:
            BranchId = branch[0]

            # Count the number of employees for the current branch
            cursor.execute("SELECT COUNT(*) FROM employees WHERE EmployeeBranchID = %s", (BranchId,))
            employee_count = cursor.fetchone()[0]

            # Update the BranchEmployeeCount for the current branch
            cursor.execute("UPDATE branches SET BranchEmployeeCount = %s WHERE BranchId = %s", (employee_count, BranchId))

        db.commit()
        print(Fore.GREEN + "Branch employee counts updated successfully." + Fore.RESET)
        log_event(db, ID, "Updated branch employee counts", True)
    except Exception as e:
        print(Fore.RED + f"Error updating branch employee counts: {e}" + Fore.RESET)
        log_event(db, ID, "Failed to update branch employee counts", False)

    sleep(1.5)
    AdminMenu(db, ID)

def ViewBranch(db, ID):
    cursor = db.cursor()

    print(Fore.GREEN + "How would you like to view the branches?" + Fore.YELLOW)
    print(Fore.BLUE + "1. Number of branches with greater or lower than a specified number of employees")
    print(Fore.BLUE + "2. Search branches by the Country or City mentioned in their address")
    print(Fore.BLUE + "3. Display all branches")
    choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))

    branch_info = ["BranchId", "BranchName", "BranchAddress", "BranchContactNumber", "BranchEmployeeCount"]

    if choice == 1:
        comparison = input(Fore.GREEN + "Do you want to view branches with greater or lower than the specified number of employees? (greater/lower): " + Fore.YELLOW).lower()
        employee_count = int(input(Fore.GREEN + "Enter the number of employees: " + Fore.YELLOW))

        if comparison == "greater":
            query = "SELECT * FROM branches WHERE BranchEmployeeCount > %s"
        elif comparison == "lower":
            query = "SELECT * FROM branches WHERE BranchEmployeeCount < %s"
        else:
            print(Fore.RED + "Invalid choice." + Fore.RESET)
            log_event(db, ID, "Invalid choice in ViewBranch", False)
            sleep(1.5)
            AdminMenu(db, ID)
            return

        try:
            cursor.execute(query, (employee_count,))
            branches = cursor.fetchall()
            if branches:
                print(Fore.GREEN + "Branch details: " + Fore.YELLOW)
                print(tabulate(branches, headers=branch_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed branches with {comparison} than {employee_count} employees", True)
            else:
                print(Fore.RED + f"No branches found with {comparison} than {employee_count} employees." + Fore.RESET)
                log_event(db, ID, f"Failed to view branches with {comparison} than {employee_count} employees", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing branches: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing branches with {comparison} than {employee_count} employees", False)

    elif choice == 2:
        location = input(Fore.GREEN + "Enter the Country or City to search in the address: " + Fore.YELLOW)

        try:
            cursor.execute("SELECT * FROM branches WHERE BranchAddress LIKE %s", ('%' + location + '%',))
            branches = cursor.fetchall()
            if branches:
                print(Fore.GREEN + "Branch details: " + Fore.YELLOW)
                print(tabulate(branches, headers=branch_info, tablefmt="pretty"))
                log_event(db, ID, f"Viewed branches with address containing {location}", True)
            else:
                print(Fore.RED + f"No branches found with address containing {location}." + Fore.RESET)
                log_event(db, ID, f"Failed to view branches with address containing {location}", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing branches: {e}" + Fore.RESET)
            log_event(db, ID, f"Error viewing branches with address containing {location}", False)

    elif choice == 3:
        try:
            cursor.execute("SELECT * FROM branches")
            branches = cursor.fetchall()
            if branches:
                print(Fore.GREEN + "All branch details: " + Fore.YELLOW)
                print(tabulate(branches, headers=branch_info, tablefmt="pretty"))
                log_event(db, ID, "Viewed all branches", True)
            else:
                print(Fore.RED + "No branches found." + Fore.RESET)
                log_event(db, ID, "Failed to view all branches", False)
        except Exception as e:
            print(Fore.RED + f"Error viewing all branches: {e}" + Fore.RESET)
            log_event(db, ID, "Error viewing all branches", False)

    else:
        print(Fore.RED + "Invalid choice." + Fore.RESET)
        log_event(db, ID, "Invalid choice in ViewBranch", False)

    sleep(1.5)
    AdminMenu(db, ID)

def CheckLogs(db, ID):
    cursor = db.cursor()

    num_logs = int(input(Fore.GREEN + "Enter the number of latest logs to display: " + Fore.YELLOW))

    try:
        cursor.execute("SELECT * FROM logs ORDER BY Occurred_At DESC LIMIT %s", (num_logs,))
        logs = cursor.fetchall()
        if logs:
            log_info = ["EmployeeID", "Event", "Occurred_At", "Status"]
            print(Fore.GREEN + "Latest logs: " + Fore.YELLOW)
            print(tabulate(logs, headers=log_info, tablefmt="pretty"))
            log_event(db, ID, f"Checked the latest {num_logs} logs", True)
        else:
            print(Fore.RED + "No logs found." + Fore.RESET)
            log_event(db, ID, f"Failed to check the latest {num_logs} logs", False)
    except Exception as e:
        print(Fore.RED + f"Error checking logs: {e}" + Fore.RESET)
        log_event(db, ID, f"Error checking the latest {num_logs} logs", False)

    sleep(1.5)
    AdminMenu(db, ID)

def ClearLogs(db, ID):
    cursor = db.cursor()

    cursor.execute("SELECT EmployeePrivilege FROM employees WHERE EmployeeID = %s", (ID,))
    Privilege = cursor.fetchone()[0]

    if Privilege != "Top_Level_Admin":
        print(Fore.RED + "You do not have the required privilege to clear logs." + Fore.RESET)
        print(Fore.RED + "Top_Level_Admin Privilege Required To Clear Logs." + Fore.RESET)
        log_event(db, ID, " ATTEMPTED TO CLEAR LOGS ".center(10," "), False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    confirmation = input(Fore.RED + "Are you sure you want to clear all logs? This action cannot be undone. (y/n): " + Fore.YELLOW).lower()
    if confirmation != 'y':
        print(Fore.RED + "Clear logs operation cancelled." + Fore.RESET)
        log_event(db, ID, "Clear logs operation cancelled", False)
        sleep(1.5)
        AdminMenu(db, ID)
        return

    try:
        cursor.execute("DELETE FROM logs")
        db.commit()
        print(Fore.GREEN + "All logs cleared successfully." + Fore.RESET)
        log_event(db, ID, "Cleared all logs", True)
    except Exception as e:
        print(Fore.RED + f"Error clearing logs: {e}" + Fore.RESET)
        log_event(db, ID, "Failed to clear logs", False)

    sleep(1.5)
    AdminMenu(db, ID)

def SaveLogs(db, ID):
    import json

    cursor = db.cursor()

    cursor.execute("SELECT EmployeeID, Event, Occurred_At, Status FROM logs")
    Logs = list(cursor.fetchall())

    Log_info = ("EmployeeID", "Event", "Occurred_At", "Status")

    formatted_logs = {}
    for index, log in enumerate(Logs):
        log = list(log)
        try:
            log[2] = log[2].strftime("%Y-%m-%d %H:%M:%S")  # Ensure Occurred_At is a datetime object
        except AttributeError:
            log[2] = str(log[2])  # Convert to string if it's not a datetime object
        log[3] = "Success" if log[3] else "Failed"

        formatted_logs[f"Log {index + 1}"] = dict(zip(Log_info, log))

    with open("Logs.json", "w") as file:
        json.dump(formatted_logs, file, indent=4)

    print(Fore.GREEN + "Logs saved to Logs.json successfully." + Fore.RESET)
    log_event(db, ID, "Saved Logs to an external file", True)

    sleep(1.5)
    AdminMenu(db, ID)

def MainMenu():
    pass

def Login():
    pass

def AdminMenu(db, ID):


    print(Fore.WHITE + "*"*20)
    print(Fore.MAGENTA + "What Would You Like To Do Next ?".center(20))
    print(Fore.BLUE + "1. Go Back To Admin Screen")
    print(Fore.BLUE + "2. Exit")
    print()

    choice = 0
    while choice not in (1, 2):
        choice = int(input(Fore.GREEN + "Enter Your Choice: " + Fore.YELLOW))

    if choice == 1: AdminScreen(db, ID)
    elif choice == 2: ProgramExit()

def log_event(db, ID, Event, Status):

    cursor = db.cursor()

    try:
        insert_query = ("INSERT INTO Logs (EmployeeID, Event, Status) VALUES (%s, %s, %s)")
        cursor.execute(insert_query, (ID, Event, Status))
        db.commit()
        print(Fore.LIGHTYELLOW_EX + "Event logged successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error logging event: {e}" + Fore.RESET)