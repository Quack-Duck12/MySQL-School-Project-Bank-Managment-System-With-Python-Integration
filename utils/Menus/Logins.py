from ..CommonScripts import *
from .AdminScreen import AdminScreen
from .CustomerScreen import CustomerScreen

from colorama import Fore

# Function to display and implement the login options
def LoginOptions(db):

    cursor = db.cursor()

    print(Fore.WHITE + "*"*20)
    # Displaying the login options
    print(Fore.BLUE + "1. Login as Admin")
    print("2. Login as Customer")
    print("3. Exit")

    print(Fore.WHITE + "*"*20)

    # Taking the choice from the user for their preferred login or exit
    choice: int = 0

    # Validating the choice
    while choice not in (1, 2, 3):
        choice = int(input(Fore.GREEN + "Enter your choice: " + Fore.YELLOW))
        if choice not in (1, 2, 3):
            print(Fore.RED + "Invalid choice, Please try again")

    print(Fore.WHITE + "*"*20)

    # Implementing the choice
    if choice == 1: AdminLogin(db)
    elif choice == 2: CustomerLogin(db)
    elif choice == 3: ProgramExit()

# Function to implement the Admin login
def AdminLogin(db):

    cursor = db.cursor()

    print(Fore.WHITE + "*"*20)
    # Taking the Employee ID and Password from the user
    ID = int(input(Fore.GREEN + "Enter the Employee ID: "  + Fore.YELLOW))
    Password = input(Fore.GREEN + f"Enter the Password for Employee ID {ID}: " + Fore.YELLOW)

    # Checking the credentials
    cursor.execute(f"SELECT EmployeePrivilege FROM Employees WHERE EmployeeID = {ID} AND EmployeePassword = '{Password}'")
    # Checking the privilege of the employee
    try: Privilege = cursor.fetchone()[0]
    except : Privilege = None

    # Implementing the privilege
    if Privilege == 'Admin' or Privilege == 'Top_Level_Admin':
        AdminScreen(db, ID)
    else:
        from time import sleep
        print(Fore.RED + "Invaild Credentials, Please try again")
        # Waiting for 1.5 seconds before displaying the login options again
        sleep(1.5)
        LoginOptions(db)

# Function to implement the User login
def CustomerLogin(db):

    cursor = db.cursor()

    print(Fore.WHITE + "*"*20)
    # Taking the Customer ID and Password from the user
    ID = int(input(Fore.GREEN + "Enter the Customer ID: "  + Fore.YELLOW))
    Password = input(Fore.GREEN + f"Enter the Password for Customer ID {ID}: " + Fore.YELLOW)

    # Checking the credentials
    cursor.execute(f"SELECT CustomerPassword FROM Customers WHERE CustomerID = {ID}")

    # Checking the Customer's Password
    try: AcctualPassword = cursor.fetchone()[0]
    except TypeError: AcctualPassword = None

    # Authenticating the user credentials
    if Password == AcctualPassword:
        CustomerScreen(db, ID)
    else:
        from time import sleep
        print(Fore.RED + "Invaild Credentials, Please try again")
        # Waiting for 1.5 seconds before displaying the login options again
        sleep(1.5)
        LoginOptions(cursor)
