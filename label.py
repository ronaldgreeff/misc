import os
from db.persistors import StoreExtract, RetrieveData

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')

fetch = RetrieveData().fetch

record = fetch(obj='record', id=1)
print(record)
