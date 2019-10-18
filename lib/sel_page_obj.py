#*-*encoding: utf-8*-*
import os, sys
import traceback
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

CURRENT_FOLDER = os.path.dirname(__file__)
PROJECT_ROOT = os.path.join(CURRENT_FOLDER, '..')

class Driver_Config():
	""" Driver options. Important to set a consistent window size."""
	options = Options()
	options.headless=True
	driver = webdriver.Firefox(firefox_options=options)
	driver.set_window_size(4000, 1600)
	# driver.maximize_window()


class SelDriver(Driver_Config):

	def __init__(self):
		self.driver = Driver_Config.driver
		self.script = open(os.path.join(CURRENT_FOLDER, 'js_extract_script.js')).read()

	def quit(self, m=None):
		print('\nq sel...{}\n'.format(m))
		self.driver.quit()

	def save_screenshot(self, screenshot_name, screenshot_folder=False):
		""" Store screenshot by given name """
		if not screenshot_folder:
			screenshot_folder = os.path.join(PROJECT_ROOT, 'screenshots')

		screenshot_location = os.path.join(
			screenshot_folder, '{}.png'.format(screenshot_name))

		self.driver.save_screenshot(screenshot_location)
		# return screenshot_location

	def process_page(self, url):
		""" """
		try:
			try:
				self.driver.get(url)
			except Exception as e:
				self.quit(m='failed to get url: {}'.format(e))

			extract = self.driver.execute_script(self.script)
			return extract # .encode('utf-8')

		except Exception as e:
			self.quit(m='failed to process_page: {}'.format(e))