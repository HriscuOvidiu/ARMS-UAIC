import os

from selenium import webdriver
from crawlers.mcmusic_crawler import MCMusicCrawler
from crawlers.flymusic_crawler import FlyMusicCrawler
from models.search_item import SearchItem
from data_processing import process_data

def pack(path):
    name = path.split(os.path.sep)[-1]
    with open(os.path.join(path, name) + '.csv', 'w+') as result:
        result.write('name, price, image')
        for f in os.listdir(path):
            if f != (name + '.csv'):
                lines = open(os.path.join(path, f), 'r').readlines()
                lines.pop(0)
                result.write(''.join(lines))

def crawl_mcmusic():
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(10)

    items = []
    items.append(SearchItem('https://www.mcmusic.ro/chitara-electrica-el', 'out/mc/electric-guitars.csv'))
    items.append(SearchItem('https://www.mcmusic.ro/acustice', 'out/mc/acoustic-guitars.csv'))
    items.append(SearchItem('https://www.mcmusic.ro/electro-acustice', 'out/mc/electro-acoustic-guitars.csv'))
    items.append(SearchItem('https://www.mcmusic.ro/electrice', 'out/mc/electric-bass.csv'))
    items.append(SearchItem('https://www.mcmusic.ro/piane-digitale-pian', 'out/mc/digital-pianos.csv'))
    items.append(SearchItem('https://www.mcmusic.ro/orgi-cu-acompaniament-o', 'out/mc/organs.csv'))
    items.append(SearchItem('https://www.mcmusic.ro/claviaturi-midi-md', 'out/mc/midi.csv'))

    crawler = MCMusicCrawler(driver)
    for i in items:
        crawler.crawl_and_save(i.url, i.out_file)

    driver.quit()

def crawl_flymusic():
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(20)

    items = []
    items.append(SearchItem('https://www.fly-music.ro/33-piane-digitale-pian-digital', 'out/fly/digital-pianos.csv'))
    items.append(SearchItem('https://www.fly-music.ro/18-chitare-chitari-electrice-chitara-electrica-seturi', 'out/fly/electric-guitars.csv'))
    items.append(SearchItem('https://www.fly-music.ro/20-chitare-chitari-acustica-chitara-seturi', 'out/fly/acoustic-guitars.csv'))
    items.append(SearchItem('https://www.fly-music.ro/21-chitare-chitari-chitara-bass-electrice-electrica', 'out/fly/electric-bass.csv'))
    items.append(SearchItem('https://www.fly-music.ro/144-sintetizatoare-sintetizator', 'out/fly/organs.csv'))
    items.append(SearchItem('https://www.fly-music.ro/80-chitare-chitari-chitara-electro-acustice--acustica-seturi', 'out/fly/electro-acoustic-guitars.csv'))
    items.append(SearchItem('https://www.fly-music.ro/239-clape-midi-claviaturi-midi', 'out/fly/midi.csv'))

    crawler = FlyMusicCrawler(driver)
    for i in items:
        crawler.crawl_and_save(i.url, i.out_file)

    driver.quit()

if __name__ == '__main__':
    # crawl_mcmusic()
    # crawl_flymusic()
    # pack('out/mc')
    # pack('out/fly')

    process_data('out/merged/', 'mc.csv', 'fly.csv')

