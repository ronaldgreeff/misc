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
            # www.boots.com > boots.com
			netloc = netloc[3:]

        # boots.com > bootscom
		folder = ''.join([i for i in netloc if i.isalnum()])

        # foo/bar/product.html -> path = [foo, bar]
		split_path = [i for i in parsed_url[2].split('/')]
		path = split_path[:-1]
		path = ''.join(path)

        # foo/bar/product.html -> file = product
		file = split_path[-1]
		file = file.split('.')[0]

		return os.path.join(SCREENSHOTS, folder, path, file)


	def crawl(self, save_screenshot=True):

		for url in self.init_urls:

			parsed_url = urlparse(url)
			location = self.screen_location(parsed_url)
			screenshot = self.selenium.save_screenshot(location)
			extract = self.selenium.process_page(url)

			yield parsed_url, screenshot, extract



if __name__ == '__main__':

	urls = google_search()

	crawler = Crawler(urls)
	for parsed_url, screenshot, extract in crawler.crawl():
		store = StoreExtract()

		store.store_data(
			parsed_url=parsed_url,
			screenshot=location,
			extract=extract)

	# continue crawling

	retriever = RetrieveData()
	retriever.site_from_url()