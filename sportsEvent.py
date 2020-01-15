import requests
from pychain.scoreScraper import get_information

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
    print(get_information(game))
