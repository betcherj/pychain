from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from urllib.parse import urlencode
import ast
import sys
import json
import flask

def get_year(SportEvent):
    return

def get_week(SportsEvent):
    return

def parse_scoreboard_data(score_board_data):
    info = {}
    return info

def get_information(SportsEvent):
    #Season type 1 is preseason
    if SportsEvent.league == 'nba':
        search_url = 'https://www.espn.com/' + SportsEvent.league + '/scoreboard/_/date/' + SportsEvent.date
        print(search_url)
    elif SportsEvent.league == "nfl":
        year = SportsEvent.date
        search_url = u'https://www.espn.com/' + SportsEvent.league + '/ scoreboard/_/year/' + SportsEvent.year + '/seasontype/2/week/' + SportsEvent.date
    else:
        print("Error Invalid League")
        return
    soup = get_html(search_url)
    divs = soup.find_all('script')
    score_board_data  =''
    for div in divs:
        if div.text[0:26] == 'window.espn.scoreboardData':
            temp = div.text.split('=', 1)[1].strip(' ').split(';')
            for i in temp:
                if i[0:30] == 'window.espn.scoreboardSettings':
                    break
                else:
                    score_board_data += i
            try:
                print(ast.literal_eval(score_board_data))
            except ValueError as ex:
                print(score_board_data)
                _exc_type, exc_value, exc_traceback = sys.exc_info()
                print("ERROR: %r" % (exc_value))
                # traceback.print_tb(exc_traceback)
                last_tb = exc_traceback
                while last_tb.tb_next:
                    last_tb = last_tb.tb_next
                print("Error location: line=%d, col=%d" % (
                    last_tb.tb_frame.f_locals["node"].lineno,
                    last_tb.tb_frame.f_locals["node"].col_offset))

            break

    #TODO Find package to parse this as a dicitonary
    info = parse_scoreboard_data(score_board_data)
    return info

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
        html_source = requests.get(url, timeout=500).text
    except Exception as e:
        print(e)
        return None
    soup = BeautifulSoup(html_source, "html.parser")
    return soup

if __name__ == "__main__":
    pass