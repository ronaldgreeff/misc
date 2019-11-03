#*-*encoding: utf-8*-*
from datetime import datetime
import peewee
from peewee import *
import pickle, json
import sys
import os
from urllib.parse import urlparse, urlunparse

from models import *

CURRENT_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(CURRENT_DIR, 'extracts.db')

database = SqliteDatabase(DB_DIR)


class BaseModel(Model):
    class Meta:
        database = database


class DataRetriever():

    def __init__(self, netloc):
        self.site = Site.get(netloc=netloc)

    def fetch_link(self):
        self.record = Record.get(
            site=self.site,
            visited=False)


if __name__ == '__main__':

    netloc = 'www.boots.com'
    dr = DataRetriever(netloc=netloc)

    ts = datetime.now()
    dr.fetch_link()
    print(dr.record.url)
    te = datetime.now()
    print('retrieved in {} secs'.format((te-ts).total_seconds()))