from Spiders.mainSpider import trigger


def find_products(route):
    name_input = input("Please enter a name")
    trigger(name_input)
