from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.orm import mapper
from db import metadata, db_session

# class Post(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(80), unique=True)
#     post_text = db.Column(db.String(255))
#
#     def __init__(self, title, filepath):
#         self.title = title
#         self.post_text = post_textdata, db_session
class Entry(object):
    query = db_session.query_property()

    def __init__(self, name=None, filePath=None, score=None):
        self.filepath = filePath
        self.name = name
        self.score = score

    def __repr__(self):
        return '<File %r>' % (self.filename)
entries = Table('entries', metadata,
    Column('eid', Integer, primary_key=True),
    Column('name', String(255), unique=True),
    Column('filepath', String(255), unique=True),
    Column('score', Float, unique=False)
)
mapper(Entry, entries)
