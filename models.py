from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import MONEY

Base = declarative_base()


# class Image(Base):
#     __tablename__ = 'images'
#     id = Column(Integer, primary_key=True)
#     identificator = Column(Integer)
    
#     def __repr__(self):
#         return "<Image(index='{}'>"\
#                 .format(self.identificator)


class Counter(Base):
    __tablename__ = 'counters'
    id = Column(Integer, primary_key=True)
    index = Column(Integer, default=0)
    
    def __repr__(self):
        return "<Counter(index='{}'>"\
                .format(self.index)
