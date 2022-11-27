
import random
from sys import exit
from controllers.user import UserCommand


def home_page(conn, cookie):
    print("""
1 - Sign In.
2 - Sign Up.
3 - Exit.\n""")
    
    entry = input("What do you want to do? --> ").lower()
    if entry == '1' or entry == "sign in":
        print("\n    -Sing in-")
        username = input("Enter Your username: ")
        password = input("Enter your password: ")
        user = UserCommand.search_by_credentials(conn, username, password)
        if user:
            cookie['user'] = user
            print(f"\nWelcome {user[4]}.")
            
    if entry == '2' or entry == "sing up":
        print("    -Sing up-\n")
        try:
            email = input("Enter your email: ").lower()
            username = input("Enter your username/nickname: ")
            password = input("Enter your password: ")
            full_name = input("Enter your full (real) name: ")
            birthday = UserCommand.input_date()
            value = {'email':email, 'username':username, 'password':password, 'full_name':full_name, 'birthday':birthday}
            UserCommand.register(conn, value)
        except Exception as err: #trabalhar melhor essa parte de tratamento de erro
            print(err)
            #print("\nEmail or username already recorded.")

    if entry == '3' or entry == 'exit':
        exit()

    if entry == "show all":
        code = random.getrandbits(16)
        print(f"Confirmation Code: {code}" )
        cod = int(input("Type the Code: "))
        if cod == code:
            print("\n      ---All Registered Accounts---\n")
            for users_registered in UserCommand.get_all(conn):
                print(users_registered)
        else:
            print("Invalid Code.")



