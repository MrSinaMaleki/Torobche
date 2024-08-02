import datetime

from .technoSpider import techno_spider
from .DigikalaSpider import digi_spider
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

                    passed_name = product["name"]
                    selected_product = list(select(p.id for p in Products if p.p_name == passed_name))
                    if selected_product:

                        # print("We had it in our db sp let's update it.")
                        temp = Products[selected_product[0]]
                        # print(product["price"])
                        temp.p_price = int(product["price"])
                        temp.p_last_update = str(datetime.now())

                    else:
                        user_id = list(select(p.id for p in Urls if p.url_address == url))

                        Products(p_name=product["name"], p_price=int(product["price"]), p_category=product["category"],
                                 p_url=product["self_url"],
                                 p_crawl_time=product["url_crawl_time"],
                                 p_seller=product["Seller"], p_img_url=product["img_url"],
                                 urls=user_id[0])

            # elif url == "https://www.digikala.com/":
            #     print("DigiKala: ")
            #     digi_info = digi_spider(search_input,0)
            #     for product in digi_info:
            #         all_infos.append(product)
            #         # print(product["name"])
            #
            #         passed_url = product["self_url"]
            #         selected_product = list(select(p.id for p in Products if p.p_url == passed_url))
            #         if selected_product:
            #             for i_d in selected_product:
            #                 print("We had it in our db sp let's update it.")
            #                 temp = Products[i_d]
            #                 print(product["price"])
            #                 temp.p_price = int(product["price"])
            #                 temp.p_last_update = str(datetime.now())
            #
            #         else:
            #             user_id = list(select(p.id for p in Urls if p.url_address == url))
            #
            #             Products(p_name=product["name"], p_price=int(product["price"]), p_category=product["category"],
            #                      p_url=product["self_url"],
            #                      p_crawl_time=product["url_crawl_time"],
            #                      p_seller=product["Seller"], p_img_url=product["img_url"],
            #                      urls=user_id[0])
        else:
            print("added: ", len(all_infos), "products")
