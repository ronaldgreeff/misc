#*-*encoding: utf-8*-*
import os, sys, io
import re
import json, pickle
import csv

PROJECT_ROOT = os.path.dirname(__file__)
DATA = os.path.join(PROJECT_ROOT, 'data')

# sys.path.append(os.path.join(PROJECT_ROOT, 'lib'))

from Database import db_manager
from Extract import sel_page_obj, utils

class Extract():

    def __init__(self):
        self.sel = sel_page_obj.SelDriver()

    def csv2dict(self):
        with open('records.csv', newline='') as csv_file:
            for row in csv.DictReader(csv_file):
                yield row

    def extract_data(self):
        # pattern description in utils.split_url()
        url_split_pattern = re.compile('^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$')

        for record in self.csv2dict():

            c = record['#']
            site = record['site']
            file = record['file']
            is_sale = record['is_sale']
            url = record['url']

            print('{}   {}\n{}\n{}\n{}\n'.format(
                c, ('is sale' if is_sale == 1 else 'not sale'), site, file, url))

            s_url = utils.split_url(url_split_pattern, url)

            screenshot_name = utils.get_screenshot_name(
                section1=s_url.group(3),
                section2=s_url.group(6))

            file_path = os.path.join(os.path.abspath(DATA), os.path.join(site, file))

            extract = self.sel.process_page('file:///' + file_path)
            # screenshot_location = self.sel.save_screenshot(screenshot_name)
            self.sel.save_screenshot(screenshot_name)

            d = os.path.join(PROJECT_ROOT, 'Database')

            with open(os.path.join(d, 'data.json'), 'w') as f:
                json.dump(extract, f, indent=4, sort_keys=True)
                
            yield s_url, extract, is_sale, screenshot_name

        self.sel.quit(m='finished extraction')


        # except Exception as e:
        #     self.sel.quit(m='failed extraction: {}'.format(e))


    def store_data(self, s_url, extract, is_sale, screenshot_name):

        db_manager.store(extract=extract, su=s_url,
            is_sale=is_sale, screenshot=screenshot_name)

    def analyse_data(self):
        pass


if __name__ == '__main__':

    db_manager.create_tables()

    e = Extract()
    for s_url, extract, is_sale, screenshot_name in e.extract_data():
        e.store_data(s_url, extract, is_sale, screenshot_name)

# EXTRACT RAW DATA
#   Extract
#   Database
#   Exploratory Analysis
# DATA PREP
#   (Cleaning, Integration, Reduction, Transformation, Discretization)
#   Labelling
#   Feature Engineering
#   Data Splitting
# MODEL TRAINING AND EVAL
#   Model Training
#   Save Trained Model
#   Evaluate Model
# PRODUCTION
#   New Data
#   Data Preparation
#   Optimal Model
#   Prediction