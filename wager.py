import sportsEvent
import json

class Wager():

    def __init__(self, sender, event, winner, amount):
        self.sender = sender
        self.event = event
        self.winner = winner
        self.amount = amount

    def toJSON(self):
        #TODO clean up this response
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


