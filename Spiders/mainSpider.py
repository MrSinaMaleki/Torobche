import datetime

from .technoSpider import techno_spider
from scripts.dbmanager import *

all_infos = []


def trigger(search_input):
    print("Crawling your data.")

    with db_session:
        urls = select(url.url_address for url in Urls)
        for url in urls:
            if url == "https://www.technolife.ir/":
                print("Techno life:")
                techno_info = techno_spider(search_input)
                for product in techno_info:
                    all_infos.append(product)
                    # print(product["name"])

                    passed_url = product["self_url"]
                    selected_product = list(select(p.id for p in Products if p.p_url == passed_url))
                    if selected_product:
                        for i_d in selected_product:
                            print("We had it in our db sp let's update it.")
                            temp = Products[i_d]
                            print(product["price"])
                            temp.p_price = str(product["price"])
                            temp.p_crawl_time = str(datetime.now())

                    else:
                        user_id = list(select(p.id for p in Urls if p.url_address == url))

                        Products(p_name=product["name"], p_price=product["price"], p_category=product["category"],
                                 p_url=product["self_url"],
                                 p_crawl_time=product["url_crawl_time"],
                                 p_seller=product["Seller"], p_img_url=product["img_url"],
                                 urls=user_id[0])

            elif url == "":
                pass
        else:
            print("added: ", len(all_infos), "products")
