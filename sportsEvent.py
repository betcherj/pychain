import requests
from scoreScraper import get_information
import json
from datetime import date

class SportsEvent():

    def __init__(self, league, teams, date):
        #TODO Reduce the number of required params
        self.league = league
        self.teams = teams
        self.result = None
        self.date = date


    def get_info(self):
        return get_information(self)


    def update_result(self):
        info = get_information(self)
        if info['status']['type']['completed']:
            info = get_information(SportsEvent)
            #TODO Finish this method
        else:
            print("Error: Event has not occured")


if __name__ == '__main__':
    game = SportsEvent('nba', ['pistons', 'cavaliers'], '20200107')
    info = get_information(game)
    print(info)

    # d = json.loads(info)
    # d['events'][0]['competitions'][0]['competitors'][0]['score']
    #   gives the score of one of the teams

