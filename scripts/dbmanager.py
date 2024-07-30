from pony.orm import *
from datetime import datetime

db = Database()


class SuperUser(db.Entity):
    username = Required(str)
    password = Required(str)


class Urls(db.Entity):
    url_address = Required(str)
    url_time_added = Required(str)


class Products(db.Entity):
    p_name = Required(str)
    p_price = Required(str)
    p_category = Required(str)
    p_url = Required(str)
    p_crawl_time = Required(str)
    p_last_update = Optional(str)
    user = Set('Users')


@db_session
def product_adder(p_name: str, p_price: str, p_category: str, p_url: str, p_crawl_time: str):
    Products(p_name=p_name, p_price=p_price, p_category=p_category, p_url = p_url, p_crawl_time= p_crawl_time)


class Users(db.Entity):
    user_name = Required(str)
    user_password = Required(str)
    products = Set(Products)


@db_session
def add_superuser(username: str, password: str):
    SuperUser(username=username, password=password)


@db_session
def url_adder(url: str):
    present = str(datetime.now())
    Urls(url_address=url, url_time_added=present)


# class Url(db.Entity):
#     url_address = Required(str)
#     add_date = Required(datetime)


db.bind(provider='postgres', user='postgres', password='1234', host='localhost', database='test101')
db.generate_mapping(create_tables=True)
# set_sql_debug(True)
