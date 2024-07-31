from pony.orm import *
from datetime import datetime

db = Database()


class Users(db.Entity):
    user_name = Required(str)
    user_password = Required(str)
    favorite = Set('Favorite')


class Favorite(db.Entity):
    f_user = Required(Users)
    f_products = Required('Products')


class Products(db.Entity):
    p_name = Required(str)
    p_price = Required(str)
    p_category = Required(str)
    p_url = Required(str)
    p_crawl_time = Required(str)
    p_seller = Required(str)
    p_img_url = Required(str)
    p_description = Optional(str)
    p_last_update = Optional(str)
    user = Set(Favorite)
    urls = Required('Urls')


@db_session
def product_adder(p_name: str, p_price: str, p_category: str, p_url: str, p_crawl_time: str, p_seller: str,
                  p_img_url: str):
    Products(p_name=p_name, p_price=p_price, p_category=p_category, p_url=p_url, p_crawl_time=p_crawl_time,
             p_seller=p_seller, p_img_url=p_img_url)


class Urls(db.Entity):
    url_address = Required(str)
    url_time_added = Required(str)
    products = Set('Products')
    url_owner = Required('SuperUser', reverse="urls")




class SuperUser(db.Entity):
    username = Required(str)
    password = Required(str)
    urls = Set(Urls, reverse="url_owner")


@db_session
def add_superuser(username: str, password: str):
    SuperUser(username=username, password=password)


@db_session
def find_element_name(name_input, msg):
    res = select(p for p in Products if name_input in p.p_name)[:]
    if res:
        print(msg)
        for product in res:
            print(
                f"name:{product.p_name}, price:{product.p_price}, category:{product.p_category} seller:{product.p_seller} \n Url:{product.p_url} \n crawled: {product.p_crawl_time} \n img-url:{product.p_img_url}",
                product.p_description, end='\n')
            print("\n")


db.bind(provider='postgres', user='postgres', password='1234', host='localhost', database='test101')
db.generate_mapping(create_tables=True)
# set_sql_debug(True)
