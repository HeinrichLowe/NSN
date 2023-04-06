from utils.connect import connect_db
from views.home import home_page
from views.logged import logged_page
from utils.migration import create_tables
from flask import Flask, request
from controllers.user import UserCommand
from exceptions.loginexception import LoginException
from exceptions.addfriendexception import AddFriendException

app = Flask(__name__)

@app.post("/signup")
def signup():
    conn = app.config["conn"]
    data = request.json
    try:
        UserCommand.register(conn, data)
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
    return return_users, 200

@app.post("/addfriend")
def addfriend():
    conn = app.config["conn"]
    data = request.json
    try:
        UserCommand.add_friend(conn, data)
    except AddFriendException as err:
        return{"message" : f"{err}"}
    return {"message" : "Congratulations, you are friends now!"}


def main():
    conn = connect_db()
    create_tables(conn)
    app.config["conn"] = conn
    app.run()

if __name__ == "__main__":
    main()
