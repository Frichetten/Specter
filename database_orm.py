# Specter BlockChain Implementation
# Nick Frichette 1/23/2017

import json

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import create_engine, exists

Base = declarative_base()


class Blocks(Base):
    __tablename__ = "blocks"
    indx = Column(Integer, primary_key=True)
    transact = Column(String(10000), nullable=False)
    previous_hash = Column(String(250), nullable=False)
    current_hash = Column(String(250), nullable=False)
    timestamp = Column(String(250), nullable=False)
    nonce = Column(String(250), nullable=False)


class Database:
    engine = create_engine('sqlite:///blockchain_db')
    session = None

    def __init__(self):
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def insert_block(self, block):
        sql_block = Blocks(
            indx=block.index,
            transact=json.dumps(block.transaction),
            previous_hash=block.previous_hash,
            current_hash=block.current_hash,
            timestamp=block.timestamp,
            nonce=block.nonce
        )
        self.session.add(sql_block)
        self.session.commit()

    def get_all_blocks(self):
        return self.session.query(Blocks).all()

    def in_db(self, block):
        (ret, ) = self.session.query(exists().where(Blocks.indx == block.index))
        return ret[0]

    def is_empty(self):
        ret = self.session.query(Blocks).count()
        if ret == 0:
            return True
        else:
            return False
