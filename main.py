from utils.MainScreen import StartScreen
import mysql.connector

def initilize():
    db = mysql.connector.connect(
        host="localhost",
        user=input("Enter your MySQL username: "),
        password=input("Enter your MySQL password: "),
    )
    cursor = db.cursor()
    try:
        cursor.execute("SHOW DATABASES LIKE 'bank'")
        result = cursor.fetchone()
        if not result:
            with open('Bank.sql', 'r') as file:
                sql_script = file.read()

            sql_statements = sql_script.split(';')

            for statement in sql_statements:
                if statement.strip():
                    cursor.execute(statement)

            db.commit()
            cursor.close()
            print('*+' * 20)
            print("Default ID = 1")
            print("Default Password = root")
    except Exception as e: print(f"Ran into error {e} while trying to initilize the program")
    
def main():
    initilize()
    StartScreen()

if __name__ == "__main__": main()