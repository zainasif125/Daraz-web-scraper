import scrapy
import json
from scrapy.crawler import CrawlerProcess
import time
import os


class TestSpider(scrapy.Spider):
    name = 'test'

    def __init__(self, query=''):
        self.query = query

    def start_requests(self):
        for i in range(1, 102):  # 102 is the total number of max pages on a product
            head = {'cookie': "JSESSIONID=67A7BD966FEDEF6A0B233309A8E7FD11"}
            api_url = f'https://www.daraz.pk/catalog/?_keyori=ss&ajax=true&clickTrackInfo=textId--2543448522407782846__abId--296224__pvid--721834c6-aa06-4851-a758-c1dceed517aa__matchType--1__srcQuery--None__spellQuery--books&from=suggest_normal&page={i}&q={self.query}&spm=a2a0e.home.search.1.35e34937dlzwzf'
            yield scrapy.Request(url=api_url, headers=head)

    def parse(self, response):
        time.sleep(2)
        resp = json.loads(response.body)
        data = resp["mods"]["listItems"]
        for info in data:
            yield {
                'name': info['name'],
                'price': info['price'],
                'img': info['image'],
            }


process = CrawlerProcess(settings={'FEED_URI': 'data.csv',
                                   'FEED_FORMAT': 'csv'})  # Data.csv is the name of the csv change it according to
# your convince
process.crawl(TestSpider, query='samsung')  # query is keyword to search for a product on daraz
process.start()
