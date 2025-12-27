import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, payment_data, prev_hash):
        self.index = index
        self.timestamp = str(datetime.now())
        self.payment_data = payment_data  # Dictionary of payment details
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Creates a SHA-256 fingerprint of the block
        block_string = json.dumps({
            "idx": self.index, 
            "data": self.payment_data, 
            "prev": self.prev_hash,
            "time": self.timestamp
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class MortgageChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, {"info": "Loan Genesis"}, "0")

    def add_payment(self, payment_data):
        prev_block = self.chain[-1]
        new_block = Block(len(self.chain), payment_data, prev_block.hash)
        self.chain.append(new_block)