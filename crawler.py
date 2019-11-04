#*-*encoding: utf-8*-*
from lib.selium_obj import Driver, extraction_script
from urllib.parse import urlparse, urlunparse
from db.persistors import StoreExtract, RetrieveData

class Crawler():
	
	def __init__(self, *urls):
		self.urls = urls
		self.selenium = selium_obj.Driver()
		self.data_store = StoreExtract()

	def get_root_folder(self, parsed_url):
		netloc = parsed_url[1]
		if 'www.' in netloc:
			netloc = netloc[3:]
		folder = netloc.split('.')[0]

	def get_filename(self, parsed_url):
		path = [i if i.isalnum() for i in parsed_url[2]]

	def info2csv(self, headers, rows, csv_file=,):
		with open(csv_file, newline='') as csv:
			for row in rows:
				csv.write(row)

	def extract2db(self,):
		pass

	def screenshot(self,):
		pass


if __name__ == '__main__':
