import time
import hashlib
import json

class Block():

    def __init__(self, index, time, wagers, previous_hash):
        self.index = index
        self.timestamp = time
        self.wagers = wagers
        self.previous_hash = previous_hash
        self.current_bets = []
        self.hash = self.hash()

    def hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string).hexdigest()


class BlockChain():
    
    def __init__(self):

        self.current_bets = []
        self.current_unmatched_bets = []
        #Genisis block
        self.chain = [Block(0, time.time(), [], '-1')]


    
    def wagers_aligned(self, wager1, wager2):
        return (wager1.event == wager2.event) \
                and (wager1.amount == wager2.amount) \
                and (wager1.winner != wager2.winner)


    def new_bet(self, wager):
        for unmatched_bet in self.current_unmatched_bets:
            if self.wagers_aligned(unmatched_bet, wager):
                self.new_block(Block(self.last_block.index, time.time(), [wager], self.last_block.hash))
                self.current_unmatched_bets.remove(unmatched_bet)
                return self.last_block.index + 1

        self.current_unmatched_bets.append(wager)

        return self.last_block.index + 1

    def new_block(self, block):
        self.chain.append(block)
        return True

    @property
    def last_block(self):
        return self.chain[-1]
