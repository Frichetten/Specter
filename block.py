# Specter Block Implementation
# Nick Frichette 12/9/2017


class Block:

    def __init__(self, index, transaction, previous_hash,
                 current_hash, timestamp, nonce):

        self.index = index
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.current_hash = current_hash
        self.timestamp = timestamp
        self.nonce = nonce


if __name__ == '__main__':
    None
