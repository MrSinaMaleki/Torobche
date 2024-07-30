from scripts.dbmanager import *

with db_session:
    urls = select(url for url in Urls)
    for url in urls:
        print(url.url_address)