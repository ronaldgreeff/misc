#*-*encoding: utf-8*-*
import os
# from lib.selium_obj import Driver, extraction_script
from urllib.parse import urlparse, urlunparse
from db.persistors import StoreExtract, RetrieveData

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
SCREENSHOTS = os.path.join(PROJECT_ROOT, 'data', 'screenshots')

class Crawler():
	
	def __init__(self, urls):
		self.init_urls = urls
		# self.selenium = selium_obj.Driver()

	def screen_location(self, parsed_url):
		netloc = parsed_url[1]
		if 'www.' in netloc:
			netloc = netloc[3:]

		folder = ''.join([i for i in netloc if i.isalnum()])

		path = parsed_url[2].split('/')

		file = path[-1]
		file = file.split('.')[0]
		# file = ''.join([i for i in file if i.isalnum()])

		file = path.split
		file = parsed_url[3].split('.')[:-1]

		return os.path.join(SCREENSHOTS, folder, path, file)


	def crawl(self, save_screenshot=True):
		for url in self.init_urls:
			parsed_url = urlparse(url)

			location = self.screen_location(parsed_url)
			print(location)

			# screenshot = self.selenium.save_screenshot(location)

			# extract = self.selenium.process_page(url)

			# store = StoreExtract()

			# store.store_data(
			# 	parsed_url=parsed_url,
			# 	screenshot=location,
			# 	extract=extract)


if __name__ == '__main__':

	urls = ['https://www.boots.com/bananas/aids/product.html', 
	'https://www.something.co.uk/bananas/boogers/product2.html', 
	'https://something.com/penis/aids/product3.html', 
	'https://something.co.uk/penis/product4.html']

	crawler = Crawler(urls)
	crawler.crawl()