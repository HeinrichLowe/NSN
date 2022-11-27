from utils.connect import connect_db
from views.home import home_page
from views.logged import logged_page
from utils.migration import create_tables

def main():
    conn = connect_db()
    create_tables(conn)
    cookie = {}

    while True:
        if "user" in cookie:
            logged_page(conn, cookie)
        else:
            home_page(conn, cookie)

if __name__ == "__main__":
    main()