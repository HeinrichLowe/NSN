from datetime import datetime
from sqlalchemy import select, insert, update, delete, or_, and_, not_
from exceptions.loginexception import LoginException
from exceptions.addfriendexception import AddFriendException
from exceptions.updateinfoexception import UpdateInfoException
from exceptions.searchbyidexception import SearchByIDException
from exceptions.finduserexception import FindUserException
from exceptions.signupexception import SignUpException
from models.users import Users
from models.friends import Friends
from sqlalchemy.sql.operators import like_op

class UserCommand:
    def get_all(conn):
        with conn.connect() as cur:
            return cur.execute(select(Users)).all()
            
    def register(conn, value):
        try:
            with conn.begin() as cur:
                sql = insert(Users).values(value)
                cur.execute(sql)
        except Exception as err:
            print(err)
            raise SignUpException()

    def update_inf(conn, user, params):
        with conn.begin() as cur:
            try:
                sql = update(Users) \
                .where(Users.id == user.id) \
                .values(params)
                cur.execute(sql)
            except Exception as err:
                print(err)
                raise UpdateInfoException()

    def search_by_credentials(conn, username, password):
        with conn.connect() as cur:
            try:
                return cur.execute(select(Users).where(Users.username==username).where(Users.password == password)).one()       
            except Exception as err:
                print(err)
                raise LoginException()
                #print("\nInvalid username or password.")

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

    def find_user(conn, name):
        with conn.connect() as cur:
            try:
                sql = cur.execute(select(Users.id, Users.full_name).where(Users.full_name.ilike(f"%{name}%")).order_by(Users.id.desc())).all()
                if sql == []:
                    raise FindUserException
                else:
                    return sql 
            except Exception as err:
                print(err)
                raise FindUserException()

    def add_friend(conn, user, friend):
        with conn.begin() as cur:
            try:
                invert = {"user_id" : f"{friend['friend_id']}", "friend_id" : f"{user['user_id']}"}
                sql1 = insert(Friends).values(user | friend)
                sql2 = insert(Friends).values(invert)
                cur.execute(sql1)
                cur.execute(sql2)
            except Exception as err:
                print(err)
                raise AddFriendException()


    def input_date():
        while True:
            try:
                bday = input("Enter your birthday (Ex: 15/06/2020): ")
                birthday = datetime.strptime(bday, "%d/%m/%Y")
                return birthday
            except:
                print("Invalid date, please, try again!")

    def search_by_id(conn, user_logged):
        with conn.connect() as cur:
            try:
                sql = select(Users).where(Users.id==user_logged)
                print(type(user_logged))
                return cur.execute(sql).one()
            except Exception as err:
                print(err)
                raise SearchByIDException()

    def search_by_friend_id(conn, friends_id):
        with conn.connect() as cur:
            try:
                sql = select(Users).where(Users.id==friends_id.user_id)
                print(type(friends_id))
                return cur.execute(sql).all()
            except Exception as err:
                print(err)
                raise SearchByIDException()

    def delete_account(conn, user):
        with conn.begin() as cur:
            try:
                sql = delete(Users).where(Users.id==user.id)
                return cur.execute(sql)
            except Exception as err:
                print(err)

    def delete_friend(conn, user, friend):
        with conn.begin() as cur:
            try:
                sql1 = delete(Friends).where(Friends.user_id==user.id, Friends.friend_id==friend.id)
                sql2 = delete(Friends).where(Friends.friend_id==user.id, Friends.user_id==friend.id)
                cur.execute(sql1)
                cur.execute(sql2)
            except Exception as err:
                print(err)

    def friends_select(conn, user):
        with conn.connect() as cur:
            try:
                sql = select(Users).where(Users.id==Friends.friend_id, Friends.friend_id!=user.id)
                return cur.execute(sql).all()
            except Exception as err:
                print(err)



    

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


