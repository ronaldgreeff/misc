#*-*encoding: utf-8*-*
import os
from datetime import datetime
from peewee import *

CURRENT_DIR = os.path.dirname(__file__)
database = SqliteDatabase(os.path.join(CURRENT_DIR, 'extracts.db'))


class BaseModel(Model):

	class Meta:
		database = database


### SITE
class Site(BaseModel):
	netloc = CharField(null=False, unique=True)

### RECORD
class Record(BaseModel):
	site = ForeignKeyField(Site, backref='records')
	url = CharField(unique=True, null=False) # extract['links'] go here
	visited = BooleanField(default=False) # for extract['links']
	screenshot = CharField(null=True)
	created = DateTimeField(default=datetime.now())
	updated = DateTimeField(default=datetime.now())
	price = DeferredForeignKey('Block', null=True)

class Title(BaseModel):
	"""
	Holds a list of titles (from page, twitter and fb)
	found, NOT the title assigned to the record
	"""
	record = ForeignKeyField(Record, backref='titles')
	title = CharField(null=True)

	# http://docs.peewee-orm.com/en/latest/peewee/models.html#primary-keys-composite-keys-and-other-tricks
	# doesn't support concept of composite foreign keys
	class Meta:
		primary_key = CompositeKey('record', 'title')

class MetaKey(BaseModel):
	name = CharField()

class MetaData(BaseModel):
	record = ForeignKeyField(Record)
	key = ForeignKeyField(MetaKey, backref='meta_data')
	val = CharField()

class Block(BaseModel):
	record = ForeignKeyField(Record)
	block_label = CharField(default='unclassified')
	block_type = CharField(null=False)
	scroll_left = CharField(null=True)
	scroll_top = CharField(null=True)
	html = TextField(null=True)
	text = TextField(null=True)
	src = CharField(null=True)

class CSSKey(BaseModel):
	key = CharField(unique=True)

class CSSVal(BaseModel):
	val = CharField(unique=True)

class Computed(BaseModel):
	block = ForeignKeyField(Block)
	key = ForeignKeyField(CSSKey)
	val = ForeignKeyField(CSSVal)

class Bound(BaseModel):
	block = ForeignKeyField(Block, primary_key=True, backref='bound')
	top = FloatField()
	left = FloatField()
	width = FloatField()
	height = FloatField()

class SelectClass(BaseModel):
	val = CharField(unique=True)
class BlockClass(BaseModel):
	block = ForeignKeyField(Block)
	val = ForeignKeyField(SelectClass)
	class Meta:
		primary_key = CompositeKey('block', 'val')

class SelectId(BaseModel):
	val = CharField(unique=True)
class BlockId(BaseModel):
	block = ForeignKeyField(Block)
	val = ForeignKeyField(SelectId)
	class Meta:
		primary_key = CompositeKey('block', 'val')

class SelectTag(BaseModel):
	val = CharField(unique=True)
class BlockTag(BaseModel):
	block = ForeignKeyField(Block)
	val = ForeignKeyField(SelectTag)