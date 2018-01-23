# Specter Block Implementation
# Nick Frichette 12/9/2017

from sqlalchemy import *
from base import Base


class Block(Base):
    __tablename__ = "blocks"
    coin_index = Column(Integer, primary_key=True)
    transaction_info = Column(String(10000), nullable=False)
    previous_hash = Column(String(250), nullable=False)
    current_hash = Column(String(250), nullable=False)
    timestamp = Column(String(250), nullable=False)
    nonce = Column(String(250), nullable=False)

    def __init__(self, coin_index, transaction_info, previous_hash,
                 current_hash, timestamp, nonce):

        self.coin_index = coin_index
        self.transaction_info = transaction_info
        self.previous_hash = previous_hash
        self.current_hash = current_hash
        self.timestamp = timestamp
        self.nonce = nonce


if __name__ == '__main__':
    None
