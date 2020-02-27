import time
import hashlib
import json

class Block():

    def __init__(self, index, time, wagers, previous_hash):
        self.index = index
        self.timestamp = time
        self.wagers = wagers
        self.previous_hash = previous_hash
        self.hash = self.hash()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def hash(self):
        block_string = self.toJSON()
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()


class BlockChain():
    
    def __init__(self):

        self.current_bets = []
        self.current_unmatched_bets = []
        #Genisis block
        self.chain = [Block(0, time.time(), [], '-1')]


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def wagers_aligned(self, wager1, wager2):
        return (wager1.event == wager2.event) \
                and (wager1.amount == wager2.amount) \
                and (wager1.winner != wager2.winner)


    def new_bet(self, wager):
        '''Places a new bet and returns True if the bet is matched'''
        for unmatched_bet in self.current_unmatched_bets:
            print("EVENT: ", end="")
            print(unmatched_bet.event == wager.event)
            print("AMOUNT: ", end="")
            print(unmatched_bet.amount == wager.amount)
            print("WINNER: ", end="")
            print(unmatched_bet.winner == wager.winner)
            if self.wagers_aligned(unmatched_bet, wager):
                self.add_block(Block(self.last_block.index, time.time(), [wager], self.last_block.hash))
                self.current_unmatched_bets.remove(unmatched_bet)
                return True

        self.current_unmatched_bets.append(wager)

        return False

    def add_block(self, block):
        self.chain.append(block)
        return True

    @property
    def last_block(self):
        return self.chain[-1]
