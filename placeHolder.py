from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
from bs4 import BeautifulSoup
import requests
import datetime
from pprint import pprint
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys


final_data = []

def digikala_spider(raw_user_input):
    browser = webdriver.Chrome()
    browser.get("https://www.digikala.com/")
    browser.maximize_window()

    standard_user_input = raw_user_input.replace(" ", "+")

    sleep(2)
    search_box = browser.find_element(By.CSS_SELECTOR,
                                      '#base_layout_desktop_fixed_header > header > div > div > div > div.flex.flex-1.items-center.grow > div > div > div > div > div > div > div > span > div')
    search_box.click()
    sleep(2)
    #
    input_box = browser.find_element(By.CSS_SELECTOR,
                                     '#base_layout_desktop_fixed_header > header > div > div > div > div.flex.flex-1.items-center.grow > div > div > div.bg-neutral-000.overflow-y-auto.rounded-medium.styles_Popper__OOG0C.shadow-modal.border-complete-200.z-2.top-0.BaseLayoutSearch_BaseLayoutSearch__popper__SGa9Y.styles_Popper--animated-active__36PO8 > div > div > div.w-full.z-1.bg-neutral-000.py-3.lg\:py-0 > div > div > div > div > div > span > label > div > div > input')
    input_box.send_keys(standard_user_input)
    sleep(2)

    input_box.send_keys(Keys.ENTER)

    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "#ProductListPagesWrapper > section.w-full.grow.relative > div.product-list_ProductList__pagesContainer__zAhrX.product-list_ProductList__pagesContainer--withSidebar__17nz1.product-list_ProductList__pagesContainer--withoutSidebar__aty9j > div > a"))
    )
    products = browser.find_elements(By.CSS_SELECTOR,
                                     "#ProductListPagesWrapper > section.w-full.grow.relative > div.product-list_ProductList__pagesContainer__zAhrX.product-list_ProductList__pagesContainer--withSidebar__17nz1.product-list_ProductList__pagesContainer--withoutSidebar__aty9j > div > a")


    product_urls = [product.get_attribute("href") for product in products][0:5]

    for product_url in product_urls:
        single_data = {"name": None, "price": None, "Seller": None, "Description": None, "category": None,
                       "img_url": None, "self_url": None, "url_crawl_time": None}
        sleep(2)
        print("getting url: ", product_url)
        browser.get(product_url)
        sleep(3)

        try:


            try:
                price_element = browser.find_element(
                    By.CSS_SELECTOR,
                    'span[data-testid="price-final"]'
                )
            except NoSuchElementException:
                price_element = browser.find_element(
                    By.CSS_SELECTOR,
                    'span[data-testid="price-no-discount"]'
                )


            single_data['self_url'] = product_url

            persian_to_english = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
            raw_price = price_element.get_attribute('innerHTML')
            translated_price = raw_price.translate(persian_to_english)

            single_data['price'] = int(translated_price.replace(",", ""))

            seller_element = browser.find_element(By.CSS_SELECTOR,
                                                  'p[class="text-neutral-700 ml-2 text-subtitle"]')
            single_data['Seller'] = seller_element.get_attribute('innerHTML')

            name_element = browser.find_element(By.CSS_SELECTOR,
                                                '#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.grow.min-w-0 > div.flex.items-center.w-full.px-5.lg\:px-0 > div > h1')
            single_data['name'] = name_element.get_attribute('innerHTML')

            img_element = browser.find_element(By.CSS_SELECTOR,
                                               '#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.lg\:ml-4.shrink-0.flex.flex-col-reverse.lg\:flex-col.styles_InfoSection__rightSection__PiYpa > div.flex.flex-col.items-center.lg\:max-w-92.xl\:max-w-145.lg\:block > div.flex.relative > div.relative.flex.items-center > div > picture > img')
            single_data['img_url'] = img_element.get_attribute('src')

            cat_element = browser.find_element(By.CSS_SELECTOR, '#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.grow.min-w-0 > div.flex.items-center.w-full.px-5.lg\:px-0 > div > div > nav > a:nth-child(2) > div > p.text-secondary-500.text-body1-strong')
            single_data['category'] = cat_element.get_attribute('innerHTML')

            try:
                desc_element = browser.find_element(By.CSS_SELECTOR,
                                                    '#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div:nth-child(6) > div.flex.w-full > div.grow.min-w-0 > article > div.text-body-1.text-neutral-800')
                single_data['Description'] = desc_element.get_attribute('innerHTML')
            except NoSuchElementException:
                single_data['Description'] = ""


            single_data['url_crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            final_data.append(single_data)
        except Exception as e:
            print("Error fetching element:", e)

    return final_data

digikala_spider()
