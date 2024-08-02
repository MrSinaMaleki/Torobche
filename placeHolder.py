from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

import datetime
from pprint import pprint
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException

from selenium.webdriver.common.keys import Keys

final_data = []


def digi_spider(raw_user_input, product_count):
    browser = webdriver.Chrome()
    standard_user_input = raw_user_input.replace(" ", "%20")
    browser.get(f"https://www.digikala.com/search/?q={standard_user_input}")
    # sleep(10)

    try:
        while True:
            sleep(5)
            products = browser.find_elements(By.CSS_SELECTOR,
                                             "#ProductListPagesWrapper > section.w-full.grow.relative > div.product-list_ProductList__pagesContainer__zAhrX.product-list_ProductList__pagesContainer--withSidebar__17nz1.product-list_ProductList__pagesContainer--withoutSidebar__aty9j > div > a")
            print(len(products), products)
            if product_count > 3:
                break

            browser.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                                   products[product_count],
                                   'target', '')

            url = products[product_count].click()
            product_count += 1
            sleep(3)

            # url = products[product_count].get_attribute("href")
            single_data = {"name": None, "price": None, "Seller": None, "Description": None, "category": None,
                           "img_url": None, "self_url": None, "url_crawl_time": None}

            single_data["name"] = browser.find_element(By.CSS_SELECTOR,
                                                       "#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.grow.min-w-0 > div.styles_InfoSection__leftSection__0vNpX > div.min-w-0.styles_InfoSection__wrapper__e2TLb.styles_InfoSection__variantInfo__PVSw4 > div:nth-child(1) > span").text
            raw_price = browser.find_element(By.CSS_SELECTOR,
                                             "#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.grow.min-w-0 > div.styles_InfoSection__leftSection__0vNpX > div.flex.flex-col.lg\:mr-3.lg\:mb-3.lg\:gap-y-2.styles_InfoSection__buyBoxContainer__3nOwP > div > div.relative.w-full.lg\:px-4.lg\:pb-2 > div > div > div > div:nth-child(1) > div.flex.justify-start.mr-auto.text-h3 > div.flex.items-center.justify-end.w-full.gap-1 > span")

            single_data["price"] = int(str(raw_price.text).replace(",", ""))
            single_data["Seller"] = browser.find_element(By.CSS_SELECTOR,
                                                         "#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.grow.min-w-0 > div.styles_InfoSection__leftSection__0vNpX > div.flex.flex-col.lg\:mr-3.lg\:mb-3.lg\:gap-y-2.styles_InfoSection__buyBoxContainer__3nOwP > div > div:nth-child(3) > a > div > div > div.flex.w-full > div > div.flex.items-center.mb-2.lg\:mb-1 > span > p").text

            single_data["category"] = browser.find_element(By.CSS_SELECTOR,
                                                           "#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.grow.min-w-0 > div.flex.items-center.w-full.px-5.lg\:px-0 > div > div > nav > a:nth-child(2) > div > p.text-secondary-500.text-body1-strong").text
            single_data["img_url"] = browser.find_element(By.CSS_SELECTOR,
                                                          "#__next > div.h-full.flex.flex-col.bg-neutral-000.items-center > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.shrink-0 > div.grow.bg-neutral-000.flex.flex-col.w-full.items-center.styles_BaseLayoutDesktop__content__hfHD1.container-4xl-w > div.lg\:px-5 > div.flex.flex-col.lg\:flex-row.overflow-hidden.styles_PdpProductContent__sectionBorder--mobile__J7liJ > div.lg\:ml-4.shrink-0.flex.flex-col-reverse.lg\:flex-col.styles_InfoSection__rightSection__PiYpa > div.flex.flex-col.items-center.lg\:max-w-92.xl\:max-w-145.lg\:block > div:nth-child(1) > div.relative.flex.items-center > div > picture > img").get_attribute(
                "src")

            single_data["self_url"] = browser.current_url
            single_data["url_crawl_time"] = str(datetime.datetime.now())
            print(single_data)
            final_data.append(single_data)

            browser.get(f"https://www.digikala.com/search/?q={standard_user_input}")
            # browser.back()




    except (ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, IndexError,
            StaleElementReferenceException) as e:
        print(e)
        digi_spider(raw_user_input, product_count=product_count + 1)
        product_count += 1

    finally:
        return final_data


# digi_spider("S24", 0)
# print(final_data)
