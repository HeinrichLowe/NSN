from utils.connect import connect_db
from views.home import home_page
from views.logged import logged_page
from utils.migration import create_tables
from flask import Flask, request
from controllers.user import UserCommand
from exceptions.loginexception import LoginException
from exceptions.addfriendexception import AddFriendException
from exceptions.searchbyidexception import SearchByIDException
from exceptions.signupexception import SignUpException
from datetime import datetime

app = Flask(__name__)

@app.post("/signup")
def signup():
    conn = app.config["conn"]
    data = request.json
    try:
        data["birthday"] = datetime.strptime(data["birthday"], "%d/%m/%Y")
        UserCommand.register(conn, data)
    except SignUpException as err:
        return{"message" : f"{err}"}, 400
    except Exception as err:
        return {"message": f"{err}"}, 400
    return {"message": "registrado"}, 201

@app.post("/signin")
def signin():
    conn = app.config["conn"]
    data = request.json
    try:
        UserCommand.search_by_credentials(conn, data['username'], data['password'])
    except LoginException as err:
        return {"message": "Invalid username or password"}, 400

    except Exception as err:
        print(err)
        return {"message": f"{err}"}, 500
    return {"message": "logged"}, 201

@app.put("/<user_logged>/change-password")
def change_password(user_logged):
    conn = app.config["conn"]
    data = request.json
    print(type(user_logged))
    try:
        user = UserCommand.search_by_id(conn, user_logged)
        UserCommand.update_inf(conn, user, data)
    except SearchByIDException as err:
        print(err)
        return {"message": f"{err}"}, 400
    except Exception as err:
        print(err)
        return {"message": f"{err}"}, 500
    return {"Message" : "Password Changed Successfully!"}, 201


@app.get("/users/<name>")
def find_users(name):
    conn = app.config["conn"]
    try:
        users = UserCommand.find_user(conn, name)
        return_users = []
        for user in users:
            return_users.append({"id" : user.id, "full_name" : user.full_name})
    except Exception as err:
        return {"message": f"{err}"}, 500
    return return_users, 201

@app.post("/<user_logged>/add-friend")
def add_friend(user_logged):
    conn = app.config["conn"]
    data = request.json
    user = {"user_id" : f"{UserCommand.search_by_id(conn, user_logged).id}"}
    try:
        UserCommand.add_friend(conn, user, data)
    except AddFriendException as err:
        return{"message" : f"{err}"}, 400
    except Exception as err:
        return {"message": f"{err}"}, 500
    return {"message" : "Congratulations, you are friends now!"}, 201

@app.delete("/<user_logged>/delete-account")
def delete_user_account(user_logged):
    conn = app.config["conn"]
    try:
        user = UserCommand.search_by_id(conn, user_logged)
        UserCommand.delete_account(conn, user)
    except Exception as err:
        return {"message": f"{err}"}, 500
    return {"message" : "Account deleted successfully!"}, 201

@app.delete("/<user_logged>/<friend_id>/delete-friend")
def delete_friend(user_logged, friend_id):
    conn = app.config["conn"]
    try:
        user = UserCommand.search_by_id(conn, user_logged)
        friend = UserCommand.search_by_id(conn, friend_id)
        UserCommand.delete_friend(conn, user, friend)
    except Exception as err:
        return {"message": f"{err}"}, 500
    return {"message" : "Successfully broken friendship!"}, 201

@app.get("/<user_logged>/friends-list")
def friends_list(user_logged):
    conn = app.config["conn"]
    try:
        friends_list = []
        user = UserCommand.search_by_id(conn, user_logged)        
        friends_id = UserCommand.friends_select(conn, user)
        for friend in friends_id:
            friends_list.append({"full_name" : friend.full_name, "id" : friend.id})
    except Exception as err:
        print(err)
    return friends_list, 201


def main():
    conn = connect_db()
    create_tables(conn)
    app.config["conn"] = conn
    app.run()

if __name__ == "__main__":
    main()
