
import sys
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Column, select, insert, update, delete, Date


class Base (DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False, unique=True)
    username: str = Column(String(64), nullable=False, unique=True)
    password: str = Column(String(32), nullable=False)
    full_name: str = Column(String(128), nullable=False)
    birthday: str = Column(Date)

def connect_db():
    return create_engine("sqlite+pysqlite:///nsn.db")

def get_all_users(conn):
    with conn.connect() as cur:
        return cur.execute(select(Users)).all()

def show_all(conn):
    users = get_all_users(conn)
    for user in users:
        print(user)

def register(conn, email, username, password, full_name, birthday):
    with conn.begin() as cur:
        sql = insert(Users).values({"email":email, "username":username, "password":password, "full_name":full_name, "birthday":birthday})
        cur.execute(sql)

def edit_email(conn, cookie):
    with conn.connect() as cur:
        temp=input("Enter your new email: ")
        try:
            verify = cur.execute(select(Users.id).where(Users.email == temp)).all()
            if not verify:
                sql = update(Users).where(Users.email == cookie['user'].email).values(email=temp)
                cur.execute(sql)
                cur.commit()
            else:
                print("\nThis email is already in use. Please try another email!")
        except Exception as err:
            print(f"Error: {err}")

def edit_username(conn, cookie):
    with conn.connect() as cur:
        temp=input("Enter your new username: ")
        try:
            verify = cur.execute(select(Users.id).where(Users.username == temp)).all()
            if not verify:
                sql = update(Users).where(Users.username == cookie['user'].username).values(username=temp)
                cur.execute(sql)
                cur.commit()
            else:
                print("\nThis username is already in use. Please try another username!")
        except Exception as err:
            print(f"Error: {err}")

def edit_password(conn, cookie):
    with conn.connect() as cur:
        temp=input("Enter your new password: ")
        try:
            old_password = input("Enter your old password: ")
            verify_old_password = cur.execute(select(Users.password).where(Users.id == cookie['user'].id)).one()
            if old_password in verify_old_password:
                sql = update(Users).where(Users.password == cookie['user'].password).values(password=temp)
                cur.execute(sql)
                cur.commit()
            else:
                print("\nOops, something is go wrong, please, try again!")
        except Exception as err:
            print(f"Error: {err}")

def edit_realname(conn, cookie):
    with conn.connect() as cur:
        temp=input("Enter your name: ")
        try:
            sql = update(Users).where(Users.full_name == cookie['user'].full_name).values(full_name=temp)
            cur.execute(sql)
            cur.commit()
        except Exception as err:
            print(f"Error: {err}")

def edit_birthday(conn, cookie):
    with conn.connect() as cur:
        temp=input("Enter your birthday (Ex: 15/06/2020): ")
        bday = datetime.strptime(temp, "%d/%m/%Y")
        try:
            sql = update(Users).where(Users.birthday == cookie['user'].birthday).values(birthday=bday)
            cur.execute(sql)
            cur.commit()
        except Exception as err:
            print(f"Error: {err}")


def login(conn, username, password):
    with conn.connect() as cur:
        try:
            user = cur.execute(select(Users).where(Users.username==username, Users.password == password)).one()
            if user:
                return user
        except:
            print("\nInvalid username or password.")

def my_profile(conn,cookie):
    with conn.connect() as cur:
        try:
            profile = cur.execute(select(Users).where(Users.id==cookie['user'].id)).one()
            return profile
        except Exception as err:
            print(err)

def create_table(conn):
    with conn.connect() as cur:
        Users.metadata.create_all(cur)

def home_page(cookie):

    conn = connect_db()
    create_table(conn)

    
    print("""
1 - Sign In.
2 - Sign Up.
3 - Exit.\n""")
    
    entry = input("What do you want to do? --> ").lower()
    if entry == '1' or entry == "sign in":
        print("\n    -Sing in-")
        username = input("Enter Your username: ")
        password = input("Enter your password: ")
        user = login(conn, username, password)
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
            bday = input("Enter your birthday (Ex: 15/06/2020): ")
            birthday = datetime.strptime(bday, "%d/%m/%Y")
            register(conn, email, username, password, full_name, birthday)
        except:
            print("\nEmail or username already recorded.")

    if entry == '3' or entry == 'exit':
        sys.exit()

    if entry == "show all":
        code = random.getrandbits(16)
        print(f"Confirmation Code: {code}" )
        cod = int(input("Type the Code: "))
        if cod == code:
            print("\n      ---All Registered Accounts---")
            show_all(conn)
        else:
            print("Invalid Code.")

def logged_page(cookie):
    conn = connect_db()
    print("""
1 - My Profile
2 - Edit my Profile
3 - Friends list
4 - Search Friends
5 - Log Out
6 - Exit.\n""")

    entry = input("What do you want to do? --> ")
    if entry == '1':
        profile = my_profile(conn, cookie)
        print(len(profile))
        print("\n   --My Profile--\n")
        print(f"Name: {profile.full_name}")
        print(f"Birthday: {profile.birthday}")
        print(f"Username: {profile.username}")
        print(f"Email: {profile.email}")
    
    if entry == '2':
        print("""
1 - Email
2 - Password
3 - User Name (Real Name)
4 - Birthday
5 - Username (Nickname/Account Name)
6 - Home Page
              """)
        entry2 = input("What do you want to edit? --> ") 
        if entry2 == "1":
            edit_email(conn, cookie)
        if entry2 == "2":
            edit_password(conn, cookie)
        if entry2 == "3":
            edit_realname(conn, cookie)
        if entry2 == "4":
            edit_birthday(conn, cookie)
        if entry2 == "5":
            edit_username(conn, cookie)

    if entry == '3':
        print("\n   -Lista de Amigos-")
    
    #if entry == '4':
        
    if entry == '5':
        print(cookie)
        cookie.pop('user')


    if entry == '6' or entry == 'exit':
        sys.exit()

def main():

    cookie = {}

    while True:
        if not cookie:
            home_page(cookie)
        else:
            logged_page(cookie)

if __name__ == "__main__":
    
    main()

