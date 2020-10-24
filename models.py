from sqlalchemy import Column, Integer, String
from database import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    path = Column(String(256), unique=True)
    tags = Column(String(512))

    def __init__(self, path, name=None, tags=None):
        self.path = path
        self.tags = tags
        if not name:
            name = path.split("/")[-1]
        self.name = name

    def __repr__(self):
        return '<Image {0}>'.format(self.name)
