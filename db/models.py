#*-*encoding: utf-8*-*
import os
from peewee import *

CURRENT_DIR = os.path.dirname(__file__)
database = SqliteDatabase(os.path.join(CURRENT_DIR, 'extracts.db'))


class BaseModel(Model):

	class Meta:
		database = database

### SITE
class Site(BaseModel):
	name = CharField(unique=True, null=False)

### URL
class URLScheme(BaseModel):
	scheme = CharField(unique=True, null=True)

class URLNetloc(BaseModel)
	netloc = CharField(unique=True, null=True)

class URLPath(BaseModel):
	path = CharField(unique=True, null=True)

class URLQuery(BaseModel):
	url = ForeignKeyField(URL)
	query = CharField(unique=True, null=True)

class URLFragment(BaseModel):
	url = ForeignKeyField(URL)
	fragment = CharField(unique=True, null=True)

class URL(BaseModel):
	site = ForeignKeyField(Site, backref='urls')
	scheme = ForeignKeyField(URLScheme)
	netloc = ForeignKeyField(URLScheme)
	path = ForeignKeyField(URLPath, null=True)
	query = ForeignKeyField(URLQuery, null=True)
	fragment = ForeignKeyField(URLFragment, null=True)

### RECORD
class Record(BaseModel):
	url = OneToOneField(URL, primary_key=True)
	date = DateTimeField()
	screenshot = CharField(null=True)
	title = OneToOneField(Block, null=True, backref='record') # title assigned to the record
	price = OneToOneField(Block, null=True)
	sale_price = OneToOneField(Block, null=True)
	rating = OneToOneField(Block, null=True)
	summary = OneToOneField(Block, null=True)

class Description(BaseModel):
	record = ForeignKeyField(Record)
	block = OneToOneField(Block, null=True)

class Review(BaseModel):
	record = ForeignKeyField(Record)
	block = OneToOneField(Block, null=True)

class Title(BaseModel):
	"""Holds a list of titles (from page, twitter and fb)
	found, NOT the title assigned to the record"""
	record = ForeignKeyField(Record, backref='titles')
	title = CharField(unique=True, null=True)

class Link(BaseModel):
	record = ForeignKeyField(Record, backref='links')
	link = CharField(unique=True, null=False)

### BLOCK
class Block(BaseModel):
	record = ForeignKeyField(Record, backref='blocks')
	block_type = CharField()
	label = CharField(null=True)
	scroll_left = CharField(null=True)
	scroll_top = CharField(null=True)
	html = TextField(null=True)
	text = TextField(null=True)
	src = CharField(null=True)


class CSSParam(BaseModel):
	name = CharField(unique=True)

class Computed(BaseModel):
	block = ForeignKeyField(Block, backref='computed')
	param = ForeignKeyField(CSSParam, backref='computed')
	value = CharField()


class Bound(BaseModel):
	block = ForeignKeyField(Block, primary_key=True, backref='bound')
	bound_top = IntegerField()
	bound_left = IntegerField()
	bound_width = IntegerField()
	bound_height = IntegerField()


class ElementID(BaseModel):
	name = CharField(unique=True)

class ElementName(BaseModel):
	name = CharField(unique=True)

class Element(BaseModel):
	block = ForeignKeyField(Block, primary_key=True, backref='element')
	element_id = ForeignKeyField(ElementID, backref='elements')
	name = ForeignKeyField(ElementName, backref='elements')

class ElemClass(BaseModel):
	elements = ManyToManyField(Element, backref='element_classes')
	name = CharField(unique=True)


class Tag(BaseModel):
	name = CharField(unique=True)

class Path(BaseModel):
	tag = ForeignKeyField(Tag, backref='paths')
	block = ForeignKeyField(Block, backref='paths')


class SelectorID(BaseModel):
	name = CharField(unique=True)

class SelectorName(BaseModel):
	name = CharField(unique=True)

# peewee.IntegrityError: UNIQUE constraint failed: 
# selecclass_selector_through.selecclass_id,
# selecclass_selector_through.selector_id

class Selector(BaseModel): #* selector_id
	block = ForeignKeyField(Block, backref='selectors')
	selector_id = ForeignKeyField(SelectorID, backref='selectors')
	name = ForeignKeyField(SelectorName, backref='selectors')

class SelecClass(BaseModel): #* selecclass_id
	# id = IntegerField(primary_key=True, unique=False,
	# 	constraints=[SQL('AUTO_INCREMENT')]) # http://docs.peewee-orm.com/en/latest/peewee/models.html#indexes-and-constraints
	selectors = ManyToManyField(Selector, backref='selector_classes')
	name = CharField(unique=True)


class MetaDataType(BaseModel):
	of_type = CharField()

class MetaData(BaseModel):
	record = ForeignKeyField(Record, backref='')
	_type = ForeignKeyField(MetaDataType, backref='meta_data')
	value = CharField()