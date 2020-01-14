from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode


def get_year(SportEvent):
    return

def get_week(SportsEvent):
    return

def get_information(SportsEvent):
    #Season type 1 is preseason
    if SportsEvent.league == 'nba':
        search_url = u'https://www.espn.com/' + SportsEvent.league + '/ scoreboard/_/date/' + SportsEvent.date
    elif SportsEvent.league == "nfl":
        year = SportsEvent.date
        search_url = u'https://www.espn.com/' + SportsEvent.league + '/ scoreboard/_/year/' + SportsEvent.year + '/seasontype/2/week/' + SportsEvent.date
    else:
        print("Error Invalid League")
        return
    soup = get_html(search_url)
    divs = soup.findAll('divs', class_ = 'sb-score final')
    if divs:
        for div in divs:
            if divs.attrs['sb-team-short'] == SportsEvent.league:
                return divs
    else:
        return None


def google_event(SportsEvent):
    search = "What is the score of the " + str(SportsEvent.teams) + " game"
    params = {'lr': 'english', 'q': search.encode('utf8'), 'start': 1, 'num': 1}
    parms = urlencode(params)
    search_url = "https://www.google.com/search?" + params
    soup = get_html(search_url)
    if soup:
        # divs = soup.findAll("div", attrs={"class": "g mnr-c g blk"})
        divs = soup.findAll("Sports Result")




def get_html(url):
    try:
        html_source = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/47.0.2526.80 Safari/537.36"}, timeout=500).text
    except Exception as e:
        print(e)
        return None
    soup = BeautifulSoup(html_source, "html.parser")
    return soup