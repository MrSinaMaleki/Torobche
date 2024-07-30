from pony.orm import *

db = Database()


class SuperUser(db.Entity):
    username = Required(str)
    password = Required(str)


@db_session
def add_superuser(username: str, password: str):
    SuperUser(username=username, password=password)


# class Url(db.Entity):
#     url_address = Required(str)
#     add_date = Required(datetime)


db.bind(provider='postgres', user='postgres', password='1234', host='localhost', database='test101')
db.generate_mapping(create_tables=True)
# set_sql_debug(True)
