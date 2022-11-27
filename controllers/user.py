from datetime import datetime
from sqlalchemy import select, insert, update, or_, and_, not_
from models.users import Users

class UserCommand:
    def get_all(conn):
        with conn.connect() as cur:
            return cur.execute(select(Users)).all()

    def add_friend(conn, user, friend):
        pass

    def register(conn, value):
        with conn.begin() as cur:
            sql = insert(Users).values(value)
            cur.execute(sql)

    def update_inf(conn, user, params):
        with conn.begin() as cur:
            try:
                sql = update(Users) \
                .where(Users.id == user.id) \
                .values(params)
                cur.execute(sql)
            except Exception as err:
                print(err)

    def search_by_credentials(conn, username, password):
        with conn.connect() as cur:
            try:
                return cur.execute(select(Users).where(Users.username==username).where(Users.password == password)).one()       
            except Exception as err:
                print(err)
                print("\nInvalid username or password.")

    def search_by_username(conn, username):
        with conn.connect() as cur:
            try:
                return cur.execute(select(Users).where(Users.username==username)).one()
            except Exception as err:
                print(err)

    def my_profile(conn,cookie):
        with conn.connect() as cur:
            try:
                profile = cur.execute(select(Users).where(Users.id==cookie['user'].id)).one()
                #profile['birthday'].strftime("%d/%m/%Y")
                return profile
            except Exception as err:
                print(err)

    def input_date():
        while True:
            try:
                bday = input("Enter your birthday (Ex: 15/06/2020): ")
                birthday = datetime.strptime(bday, "%d/%m/%Y")
                return birthday
            except:
                print("Invalid date, please, try again!")


    

"""
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
"""


