from time import sleep
from scripts.dbmanager import *
from getpass import getpass
from core.state import Auth
from core.utils import safe


@safe
def login(route):
    with db_session:
        username_inp = input("Please enter username: ")
        assert username_inp, "Username should not be empty !"

        password_inp = getpass("Please enter password: ")
        assert password_inp, "Password should not be empty !"

        admin = SuperUser.get(username=username_inp, password=password_inp)

        if admin:
            Auth.admin_login_status = True
            Auth.user = username_inp
            print(f"\n\nWelcome '{username_inp.title()}' ⭐ ")
            sleep(2)
        else:
            raise ValueError("Username or password invalid !")


def logout(route):
    Auth.admin_login_status = False


def add_url(route):
    url_address = input("Please enter a URL-Address. ")
    assert url_address, "URL address can not be empty !"
    with db_session:
        if not(select(p for p in Urls if p.url_address == url_address)):
            user_id = list(select(p.id for p in SuperUser if p.username == Auth.user))
            print(user_id[0])

            present = str(datetime.now())
            Urls(url_address=url_address, url_owner=user_id[0], url_time_added=present)

            print(f"Added '{url_address}' to the database successfully!")
            sleep(1)
        else:
            print("The Url has already been added!")


def delete_url(route):
    url_address_inp = input("Please enter a URL-Address. ")
    assert url_address_inp, "URL address can not be empty !"
    with db_session:
        if select(p for p in Urls if p.url_address == url_address_inp):
            Urls.select(lambda p: p.url_address == url_address_inp).delete(bulk=True)
            print(f"deleted '{url_address_inp}' from the database successfully!")
        else:
            print("The url hasn't been added !")
            sleep(1)
