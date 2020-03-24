import csv

class Crawler():

    def __init__(self, driver):
        self.driver = driver
        self.rows = ['name', 'price', 'image'] 

    def _crawl(self, path, driver):
        products = []
        self.driver.get(path)
        should_stop = False

        while not should_stop:
            products.extend(self._get_products_from_current_page(self.driver))
            should_stop = self._go_to_next_page(self.driver)

        return products

    def crawl_and_save(self, path, out_file):
        products = self._crawl(path, self.driver)

        with open(out_file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.rows)

            for p in products:
                writer.writerow([p.name, p.price, p.image])
        