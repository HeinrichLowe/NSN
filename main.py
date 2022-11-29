from utils.connect import connect_db
from views.home import home_page
from views.logged import logged_page
from utils.migration import create_tables
from flask import Flask, request, Response
from controllers.user import UserCommand

app = Flask(__name__)

@app.post("/signup")
def signup():
    conn = app.config["conn"]
    data = request.json
    try:
        UserCommand.register(conn, data)
    except Exception as err:
        return {"message": "email já cadastrado"}, 400
    return {"message": "registrado"}, 201

@app.post("/signin")
def signin():
    conn = app.config["conn"]
    data = request.json
    try:
        UserCommand.search_by_credentials(conn, data['username'], data['password'])
    except Exception as err:
        #print(err)
        return {"message": "Invalid username or password"}, 400
    return {"message": "logged"}, 201

def main():
    conn = connect_db()
    create_tables(conn)
    app.config["conn"] = conn
    app.run()

if __name__ == "__main__":
    main()
