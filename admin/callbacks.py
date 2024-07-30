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

        print("Admin procces just begins!")
        admin = SuperUser.get(username=username_inp, password=password_inp)
        print("This is admin: ", admin)
        sleep(4)

        if admin:
            Auth.login_status = True
            Auth.user = username_inp
            print(f"\n\nWelcome '{username_inp.title()}' ⭐ ")
            sleep(4)
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
    print("In Logout Callbacks")
    Auth.login_status = False
