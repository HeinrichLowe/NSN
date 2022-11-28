from sys import exit
from controllers.user import UserCommand




def logged_page(conn, cookie):
    print("""
1 - My Profile
2 - Edit my Profile
3 - Friends List
4 - Search Friends
5 - Log Out
6 - Exit\n""")

    entry = input("What do you want to do? --> ").lower()
    if entry == '1' or entry == 'my profile':
        profile = UserCommand.my_profile(conn, cookie)
        #print(len(profile))
        print("\n    --My Profile--\n")
        print(f"Name: {profile.full_name}")
        print(f"Birthday: {profile.birthday.strftime('%d/%m/%Y')}")
        print(f"Username: {profile.username}")
        print(f"Email: {profile.email}")
    
    if entry == '2' or entry == 'edit my profile':
        print("""
1 - Email
2 - Password
3 - User Name (Real Name)
4 - Birthday
5 - Username (Nickname/Account Name)
6 - Home Page
              """)
        entry2 = input("What do you want to edit? --> ") 
        if entry2 == "1" or entry2 == "email":
            temp = input("Enter your new email: ")
            UserCommand.update_inf(conn, cookie['user'], {"email": temp})
        if entry2 == "2" or entry2 == "password":
            temp1 = input("\nCurrent password: ")
            temp2 = input("New Password: ")
            temp3 = input("Confirm your new password: ")
            try: #fazer função ↓
                if temp1 == cookie['user'].password and temp2 == temp3:
                    UserCommand.update_inf(conn, cookie['user'], {"password": temp2})
                    print("\nPassword changed successfully.")
                elif temp1 != cookie['user'].password:
                    print("\nInvalid current password, please try again.")
                elif temp2 != temp3:
                    print("\nThe new passwords do not match, please try again.")
            except Exception as err:
                print(err)
        if entry2 == "3" or entry2 == "user name":
            temp = input("Enter your name: ")
            UserCommand.update_inf(conn, cookie['user'], {"full_name": temp})
        if entry2 == "4" or entry2 == "birthday":
            temp = UserCommand.input_date()
            UserCommand.update_inf(conn, cookie['user'], {"birthday": temp})
        if entry2 == "5" or entry2 == "username":
            try: #fazer função ↓
                temp1 = input("\nEnter your new username: ")
                temp2 = input("Enter your password to confirm: ")
                if temp2 == cookie["user"].password:
                    UserCommand.update_inf(conn, cookie['user'], {"username": temp1})
                    print("\nUsername changed sucefully.")
                else:
                    print("\nInvalid password.")
            except Exception as err:
                print(err)

    if entry == '3' or entry == 'friends list':
        print("\n   -Lista de Amigos-")
    
    #if entry == '4' or entry == 'search friends':
        
    if entry == '5' or entry == 'log out':
        #print(cookie)
        cookie.pop('user')


    if entry == '6' or entry == 'exit':
        exit()

    if entry == '7':
        print(type(cookie['user'].id))