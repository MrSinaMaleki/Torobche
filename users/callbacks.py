from Spiders.mainSpider import trigger
from core.utils import clear
from scripts.dbmanager import *
from getpass import getpass
from core.utils import safe
from core.state import Auth
from time import sleep


@safe
def login(route):
    with db_session:
        username_inp = input("Please enter username: ")
        assert username_inp, "Username should not be empty !"

        password_inp = getpass("Please enter password: ")
        assert password_inp, "Password should not be empty !"

        user = Users.get(user_name=username_inp, user_password=password_inp)

        if user:
            Auth.user_login_status = True
            Auth.user = username_inp
            print(f"\n\nWelcome '{username_inp.title()}' ⭐ ")
            sleep(2)
        else:
            raise ValueError("Username or password invalid !")


@safe
def register(route):
    with db_session:
        username = input("Please enter username: ")
        assert username, "Username should not be empty !"

        password = getpass("Please enter password: ")
        assert password, "Password should not be empty !"

        confirm_password = getpass("Please re-enter password: ")
        assert confirm_password, "Confirm Password should not be empty !"
        assert confirm_password == password, "Confirm password and password doesn't match !"

        Users(user_name=username, user_password=password)
        print("Register Successful ✅ ")


def find_products(route):
    name_input = input("Please enter The name of the product you want me to find. \n")
    with db_session:
        find_element_name(name_input=name_input, msg="Here is the data we found in our db:")

        flag = input("Would you like new data we can also search in a bunch of websites.")
        if flag.lower() != "no":
            clear()
            trigger(search_input=name_input)

            clear()
            print("\n")
            print("Here is all new data + old ones")
        else:

            find_element_name(name_input=name_input, msg=" ")


def find_by_category(Route):
    category_input = input("Please enter The Category of the product you want me to find. \n")
    with db_session:
        find_element_category(category_input=category_input, msg="Here is the data we found in our db:")

        flag = input("Would you like new data we can also search in a bunch of websites.")
        if flag.lower() != "no":
            clear()
            trigger(search_input=category_input)

        clear()
        print("\n")
        print("Here is all new data + old ones")

        find_element_category(category_input=category_input, msg=" ")


def add_favorite(Route):
    with db_session:
        user_id = list(select(u.id for u in Users if u.user_name == Auth.user))

        url_inp = input("Please enter the url address of the element you want to add. \n")

        product_id = list(select(p.id for p in Products if p.p_url == url_inp))

        print(user_id, product_id)

        Favorite(f_user=user_id[0], f_products=product_id[0])
        print("Added to your list!")
        # print("Here is your list.\n")


def see_favorites(Route):
    with db_session:
        user_id = list(select(u.id for u in Users if u.user_name == Auth.user))
        user_object = Users.get(id=user_id[0])

        products = list(select(p.f_products for p in Favorite if p.f_user == user_object))
        for user in products:
            print(user.p_url)


def find_by_price(Route):
    start_price = input("start price: ")
    if not start_price:
        start_price = 0

    max_price = int(input("max price: "))
    assert max_price, "max price should not be empty !"

    with db_session:
        products_list = list(select(p.p_url for p in Products if between(p.p_price, int(start_price), max_price)))
        for product in products_list:
            print(product)

