from colorama import Fore

# Function to exit the program
def ProgramExit():
    from colorama import Fore
    from pyfiglet import figlet_format

    Exit_Text = figlet_format('Thank you for choosing Gringotts Bank, Have a nice day!',font= 'stop')

    print(Fore.LIGHTMAGENTA_EX + Exit_Text)
    exit()