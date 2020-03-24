from models.product import Product
import csv
from .crawler import Crawler

class MCMusicCrawler(Crawler):

    def __init__(self, driver):
        super().__init__(driver)

    def _go_to_next_page(self, driver):
        page_buttons = driver.find_elements_by_class_name('pagination')
        if len(page_buttons) == 0:
            return True
            
        page_buttons = page_buttons[0].find_elements_by_tag_name('li')
        page_buttons = list(map(lambda x: x.find_elements_by_tag_name('a')[0] if 'a' in x.get_attribute('innerHTML') else None, page_buttons))
        page_buttons = list(filter(lambda x: x, page_buttons))

        current_page_index = 0
        for (i, b) in enumerate(page_buttons):
            if 'active' in b.get_attribute('class'):
                current_page_index = i
                break
        
        if current_page_index + 1 >= len(page_buttons):
            return True

        driver.execute_script("arguments[0].click();", page_buttons[current_page_index + 1])
        
        return False

    def _get_products_from_current_page(self, driver):
        products = []
        
        els = driver.find_elements_by_class_name('product-box')

        for e in els:
            name = e.find_elements_by_class_name('top-side-box')[0].find_element_by_tag_name('a').text
            price = e.find_elements_by_class_name('top-side-box')[0].find_elements_by_class_name('price')[0].find_elements_by_class_name('text-main')
            image = e.find_elements_by_class_name('image-holder')[0].find_element_by_tag_name('img').get_attribute('src')
            if len(price):
                price = price[0].text
            product = Product(name, price, image)
            products.append(product)

        return products
        