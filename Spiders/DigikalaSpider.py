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


def digi_spider(raw_user_input):
    browser = webdriver.Chrome()
    standard_user_input = raw_user_input.replace(" ", "%20")
    browser.get(f"https://www.digikala.com/search/?q={standard_user_input}")
    # sleep(10)

    product_count = 0
    try:
        while True:
            sleep(4)
            products = browser.find_elements(By.CSS_SELECTOR, 'div[class="product-list_ProductList__item__LiiNI"] > a')
            if product_count >= 5:
                break

            browser.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                                   products[product_count],
                                   'target', '')

            products[product_count].click()
            product_count += 1
            sleep(1)

            url = products[product_count].get_attribute("href")

            price = browser.find_element(By.CSS_SELECTOR, '#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.grow.min-w-0 > div.styles_InfoSection__leftSection__0vNpX > div.flex.flex-col.lg\:mr-3.lg\:mb-3.lg\:gap-y-2.styles_InfoSection__buyBoxContainer__3nOwP > div > div.relative.w-full.lg\:px-4.lg\:pb-2 > div > div > div > div:nth-child(1) > div > div.flex.items-center.justify-end.w-full.gap-1 > span').text
            print(price)



            browser.back()




    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, IndexError,
            StaleElementReferenceException) as e:
        print(e)
        digi_spider(raw_user_input)
        product_count += 1


digi_spider("s24 ultra")
