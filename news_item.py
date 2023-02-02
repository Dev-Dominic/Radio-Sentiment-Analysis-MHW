from marshmallow import Schema, fields

class NewsItem(object):
    def __init__(self, title, date, text):
        self.title = title
        self.date = date
        self.text = text
        self.sentimentScore = None
        

class NewsItemSchema(Schema):
    title = fields.Str()
    date = fields.Date()
    text = fields.Str()
    sentimentScore = fields.Number()
