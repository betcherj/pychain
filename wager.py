import sportsEvent
import json

class Wager():

    def __init__(self, sender, event, winner, amount):
        self.sender = sender
        self.event = event
        self.winner = winner
        self.amount = amount
