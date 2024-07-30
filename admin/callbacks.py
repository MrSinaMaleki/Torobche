from time import sleep
# from models import User
from scripts.dbmanager import *
from getpass import getpass
from core.state import Auth
from core.utils import safe


@safe
def login(route):
    with db_session:
        username_inp = input("Please enter username: ")
        assert username_inp, "Username should not be empty !"

        password_inp = input("Please enter password: ")
        assert password_inp, "Password should not be empty !"

        admin = SuperUser.get(username=username_inp, password=password_inp)

        if admin:
            Auth.admin_login_status = True
            Auth.user = username_inp
            print(f"\n\nWelcome '{username_inp.title()}' ⭐ ")
            sleep(2)
        else:
            raise ValueError("Username or password invalid !")


@safe
def register(route):
    username = input("Please enter username: ").strip().lower()
    assert username, "Username should not be empty !"

    password = getpass("Please enter password: ")
    assert password, "Password should not be empty !"

    confirm_password = getpass("Please re-enter password: ")
    assert confirm_password, "Confirm Password should not be empty !"
    assert confirm_password == password, "Confirm password and password doesn't match !"

    # User(username, password)
    print("Register Successful ✅ ")


def logout(route):
    Auth.admin_login_status = False


def add_url(route):
    url_address = input("Please enter a URL-Address. ")
    assert url_address, "URL address can not be empty !"

    url_adder(url=url_address)
    print(f"Added '{url_address}' to the database successfully!")
    sleep(1)


def delete_url(route):
    url_address_inp = input("Please enter a URL-Address. ")
    assert url_address_inp, "URL address can not be empty !"
    with db_session:
        Urls.select(lambda p: p.url_address == url_address_inp).delete(bulk=True)
    print(f"deleted '{url_address_inp}' from the database successfully!")
    sleep(1)
