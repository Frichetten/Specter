# Specter BlockChain Implementation
# Nick Frichette 1/23/2017

import json

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy import create_engine, exists

from base import Base
from block import *


class Database:
    engine = create_engine('sqlite:///blockchain_db')
    session = None

    def __init__(self):
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def insert_block(self, block):
        sql_block = Block(
            block.coin_index,
            json.dumps(block.transaction_info),
            block.previous_hash,
            block.current_hash,
            block.timestamp,
            block.nonce
        )
        self.session.add(sql_block)
        self.session.commit()

    def get_all_blocks(self):
        return self.session.query(Block).all()

    def in_db(self, block):
        (ret, ) = self.session.query(exists().where(Block.coin_index == block.coin_index))
        return ret[0]

    def is_empty(self):
        ret = self.session.query(Block).count()
        if ret == 0:
            return True
        else:
            return False
