import time

class BlockChain():
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        #Genisis block

        self.new_block = new_block(prev_hash="1", proof =100)
    

    def new_block(self, proof, previous_hash):
        block = {
            'index' = len(self.chain) +1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
            }
        self.current_transactions =[]

        self.chain.append(block)
        return block
    
    
    def new_transaction(self, sender, recipient, ammount):

        self.current_transactions.append({
            'sender' = sender,
            'recipient' = recipient,
            'ammount' = ammount,
            })

        return self.last_block['index'] + 1
    @property
    def lastBlock(self):
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha25(block_string).hexdigest()

    def proof_of_word(self, last_block):
        
        


    



        
        
    
    
