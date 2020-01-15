import requests
from scoreScraper import get_information
import json
class SportsEvent():

    def __init__(self, league, teams, date):
        self.league = league
        self.teams = teams
        self.result = None
        self.date = date

    def get_info(self):
        return get_information(self)


if __name__ == '__main__':
    game = SportsEvent('nba', ['pistons', 'cavaliers'], '20200107')
    info = get_information(game)

    print(json.loads(info))

    # d = json.loads(info)
    # d['events'][0]['competitions'][0]['competitors'][0]['score']
    #   gives the score of one of the teams

