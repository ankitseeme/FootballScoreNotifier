from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess as s
import time
from urllib.error import HTTPError


def getbsObj(url):
    try:
        html = urlopen(url,timeout=100)
    except HTTPError as e:
        print("HTTPError")
        exit(2)
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
    except:
        print("Parsing Error")
    return bsObj


def get_team(bsObj):
    try:
        team1 = bsObj.findAll('span', {'class':
                                'widget-match-header__name--full'})[0].text
        team2 = bsObj.findAll('span', {'class':
                            'widget-match-header__name--full'})[1].text
    except:
        print("""Parsing Error... Error during team name extraction... """\
            """Doesn't seem to be a valid match URL""")
        exit(3)
    return team1, team2


def get_score(bsObj):
    try:
        score = bsObj.find('span',
                           {'data-slot': 'score'}).text
        timest = bsObj.find('span',
                            {'data-slot': 'state'}).text
    except:
        print("""Parsing Error... Error  during score extraction... """\
            """Doesn't seem to be a valid match URL""")
        exit(4)
    return score, timest


def check_FT(score, timing, team1, team2):
    if (timing == 'FT'):
        print("Game has Finished")
        if (int(score.split('-')[0]) > int(score.split('-')[1])):
            heading = team1 + " Won"
        elif (int(score.split('-')[0]) == int(score.split('-')[1])):
            heading = "Drawn"
        else:
            heading = team2 + " Won"
        final_score = team1 + " " + score.split('-')[0] + "  -  " + score.split('-')[1] + " " + team2
        notify(heading, final_score)
        print("Exiting...")
        exit(0)


def compare_score(prevscore, score):
    if score != prevscore:
        t1score = score.split('-')[0]
        t2score = score.split('-')[1]
        if t1score != prevscore.split('-')[0]:
            return 1
        else:
            return 2
    else:
        return 0


def notify(head, msg):
    s.call(['notify-send', head, msg])


if __name__ == "__main__":
    try:
        url = input("Provide the GOAL.com match link : ")
    except:
        print("URL Input error... Please Try again")
        exit(1)
    bsObj = getbsObj(url)
    team1, team2 = get_team(bsObj)
    score, timest = get_score(bsObj)
    print(team1 + " VS " + team2)
    print(timest + " : " + score)
    while True:
        bsObj = getbsObj(url)
        prevscore = score
        score, timest = get_score(bsObj)
        check_FT(score, timest, team1, team2)
        time.sleep(30)
        print(timest + " : " + score)
        res = compare_score(prevscore, score)
        if res == 1:
            print(str(team1) + " scored")
            notify(str(team1) + " scored", score)
        elif res == 2:
            print(str(team2) + " scored")
            notify(str(team2) + " scored", score)

