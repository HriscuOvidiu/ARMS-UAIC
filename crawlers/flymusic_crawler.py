from models.product import Product
from .crawler import Crawler
import time

class FlyMusicCrawler(Crawler):

    def __init__(self, driver):
        # super().__init__(driver)
        Crawler.__init__(self, driver)

    def _go_to_next_page(self, driver):
        try:
            pags = driver.find_element_by_id('pagination').find_elements_by_tag_name('li')
        except:
            return True

        if len(pags) > 2:
            pags.pop()
            pags.pop(0)
        current_page_index = 0

        for (i, p) in enumerate(pags):
            if 'current' in p.get_attribute('class'):
                current_page_index = i
                break
        
        if current_page_index + 1 >= len(pags):
            return True

        click_el = pags[current_page_index + 1].find_element_by_tag_name('a')
        driver.execute_script("arguments[0].click();", click_el)
        
        return False

    def _get_products_from_current_page(self, driver):
        products = []

        time.sleep(3)
        try:
            subcategories = driver.find_element_by_id('subcategories')
            subcategories = subcategories.find_elements_by_tag_name('li')
            subcategories = list(map(lambda x: x.find_element_by_tag_name('a').get_attribute('href'), subcategories))
            for c in subcategories:
                products.extend(self._crawl(c, driver))
            return products
        except:
            els = driver.find_elements_by_class_name('ajax_block_product')
            for e in els:
                name = e.find_elements_by_class_name('s_title_block')[0].find_element_by_tag_name('a').text
                price = e.find_elements_by_class_name('price')[0].text
                image = e.find_elements_by_class_name('front-image')[0].get_attribute('src')

                products.append(Product(name, price, image))
            
            return products
        