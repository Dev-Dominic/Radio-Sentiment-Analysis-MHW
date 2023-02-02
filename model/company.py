from marshmallow import Schema, fields
from .news_item import NewsItemSchema

        
class Company(object):
    def __init__(self, name):
        self.name = name
        self.newsItems = []
    


class CompanySchema(Schema):
    name = fields.Str()
    newsItems = fields.Nested(NewsItemSchema)
