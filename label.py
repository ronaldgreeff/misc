import os
from db.persistors import StoreExtract, RetrieveData

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')

retreive = RetrieveData()

record = retrieve.fetch(obj='Record', id=1)

