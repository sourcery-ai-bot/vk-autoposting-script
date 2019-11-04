from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import MONEY

Base = declarative_base()


class Posting(Base):
    __tablename__ = 'postings'
    id = Column(Integer, primary_key=True)
    offset_counter = Column(Integer)
    group = Column(Integer)
    day = Column(Integer)
    
    def __repr__(self):
        return "<Posting(offset_counter='{}', group='{}', day={})>"\
                .format(self.offset_counter, self.group, self.day)
