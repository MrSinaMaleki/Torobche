from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import requests
import datetime
from pprint import pprint
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException

from selenium.webdriver.common.keys import Keys

final_data = []


def techno_spider(raw_user_input):
    browser = webdriver.Chrome()
    browser.get("https://www.technolife.ir/")

    # raw_user_input = "This is just a test!"
    standard_user_input = raw_user_input.replace(" ", "+")

    product_count = 0

    try:
        search_box = browser.find_element(By.CSS_SELECTOR,
                                          '#__next > div.w-full > header > div > div > div > div > nav > div.transition-all.relative > div > div.h-auto.w-auto > div')
        search_box.click()

        input_box = browser.find_element(By.CSS_SELECTOR,
                                         '#__next > div.w-full > header > div > div > div > div > nav > div.transition-all.z-\[1001\].relative > div > div.h-auto.w-auto > div > input')
        input_box.send_keys(raw_user_input)
        sleep(1)

        input_box.send_keys(Keys.ENTER)
        sleep(2)

        while True:
            sleep(2)
            products = browser.find_elements(By.CSS_SELECTOR, "article > section > div > :nth-child(2) > a")
            # print(len(products))

            if product_count >= 5:
                break
            browser.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                                   products[product_count],
                                   'target', '')

            url = products[product_count].get_attribute("href")
            r = requests.get(url)
            try:
                price_soup = BeautifulSoup(r.content, 'html5lib').find('p', attrs={
                    "class": "text-[19px] font-semiBold !leading-5 xl:text-[22px] text-red-600"}).encode_contents()
            except Exception as e:
                # print("Exception handled!")
                price_soup = BeautifulSoup(r.content, 'html5lib').find('p', attrs={
                    "class": "text-[19px] font-semiBold !leading-5 xl:text-[22px] text-gray-800"}).encode_contents()

            seller_soup = BeautifulSoup(r.content, 'html5lib').find('p', attrs={
                "class": "mr-4 2md:mr-2 xl:mr-4 text-[15px] 2md:text-xss xl:text-[15px] font-medium text-gray-700"}).text


            products[product_count].click()
            sleep(2)

            single_data = {"name": None, "price": None, "Seller": None, "Description": None, "category": None,
                           "img_url": None, "self_url": None, "url_crawl_time": None}

            single_data["img_url"] = browser.find_element(By.CSS_SELECTOR, ".pdpMagnify + img").get_attribute("src")
            single_data["name"] = browser.find_element(By.CSS_SELECTOR, "h2").text
            single_data["Description"] = browser.find_element(By.CSS_SELECTOR, "h1").text
            single_data["category"] = browser.find_element(By.CSS_SELECTOR,
                                                           "#__next > div.w-full > main > div > div > nav > ul > li:nth-child(4) > a").text
            single_data["price"] = str(str(price_soup).replace(",", "").replace("b'", "").replace("'", ""))
            single_data["Seller"] = str(seller_soup)
            single_data["self_url"] = url
            single_data["url_crawl_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(single_data)
            final_data.append(single_data)

            product_count += 1

            browser.get(f"https://www.technolife.ir/product/list/search?keywords={standard_user_input}")
            # browser.back()

    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, IndexError,
            StaleElementReferenceException) as e:
        print(e)
        techno_spider(raw_user_input)
        product_count += 1

    finally:
        return final_data
