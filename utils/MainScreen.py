#Importing the required modules
from .Menus.Logins import *

import mysql.connector
from pyfiglet import figlet_format
from colorama import Fore

# Function to display the start screen
def StartScreen():

    db = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="root",
    database="bank",
    )

    Welcome_Text = figlet_format('Gringotts Bank Managment Portal',font= 'stop')
    print(Fore.CYAN + Welcome_Text)

    LoginOptions(db)