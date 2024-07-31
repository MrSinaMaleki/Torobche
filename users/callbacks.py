from Spiders.mainSpider import trigger
from scripts.dbmanager import *
from os import system as terminal, name as os_name
from core.utils import clear


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

        find_element_name(name_input=name_input, msg=" ")


