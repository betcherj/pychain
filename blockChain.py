import time
import hashlib
import json


class BlockChain():
    
    def __init__(self):
        self.chain = []
        self.current_bets = []
        self.current_unmatched_bets = []
        self.chain = []
        #Genisis block

        self.new_block(previous_hash=1, proof =100)


    def new_block(self, previous_hash, proof):
        block = {
            'index' : len(self.chain) +1,
            'timestamp' :  time.time(),
            'wagers' : self.current_bets,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
            }
        self.current_bets = []
        self.chain.append(block)

        return block

    def new_bet(self, wager):
        for i in range(len(self.current_unmatched_bets)):
            if self.current_unmatched_bets[i].event == wager.event and self.current_unmatched_bets[i].winner != wager.winner and self.current_unmatched_bets[i].amount == wager.amount:
                self.current_bets.extend(
                    [self.current_unmatched_bets[i].toJSON(), wager.toJSON()]
                )
                self.current_unmatched_bets = self.current_unmatched_bets[:i] + self.current_unmatched_bets[i+1:]
                return self.last_block['index'] + 1
        self.current_unmatched_bets.append(
            wager
        )
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        #Sorted to make sure we have
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) == False:
            proof +=1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = ('{' + str(last_proof) + str(proof) + '}').encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '1234'



        
        


    



        
        
    
    
