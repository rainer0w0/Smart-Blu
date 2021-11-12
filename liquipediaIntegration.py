import requests
from requests.auth import HTTPBasicAuth
import datetime
from datetime import date, timedelta


today = date.today()
tomorrow = datetime.datetime(today.year,today.month,today.day+1)
today = today.strftime("%d-%m-%Y")
tomorrow = tomorrow.strftime("%d-%m-%Y")
APIKEY = 'API KEY GOES HERE'
headers={'authorization': 'Apikey ' + APIKEY}
params= {'wiki': 'counterstrike', 'date': (today)}


def checktransfers(): #Returns a list of transfers for the day
    fulltransfer = ""
    listoftransfers = []
    url = "https://api.liquipedia.net/api/v2/transfer"
    params= {'wiki': 'counterstrike', 'conditions':'[[date::' + today + ']]'}
    response = requests.get(url,headers=headers,params=params)
    jsonboy = response.json()
    jsonboy = jsonboy.get('result', [])
    for trans in jsonboy:
        player = trans.get('player')
        if checkPlayer(player):
            t1 = trans.get('fromteam')
            t2 = trans.get('toteam')
            fulltransfer = f"{player},{t1},{t2}"
            listoftransfers.append(fulltransfer)
    return listoftransfers






def checkPlayer(player): #Checks to see if the player has a page on Liquipedia (So it only returns "important" players)
    #Capitalizes first letter of string
    player = list(player)
    player[0] = player[0].upper()
    player = ''.join(player)
    url = "https://api.liquipedia.net/api/v2/player"
    params= {'wiki': 'counterstrike', 'conditions':'[[pagename::'+player+']]'}
    playerresponse = requests.get(url,headers=headers,params=params)
    jsondude = playerresponse.json()
    jsondude = jsondude.get('result',[])
    try:
        if jsondude[0].get('player') == None:
            return True
        else:
            return False
    except IndexError:
        return False



def checkifGame(team): ## no longer need work :) WILL RETURN THE TIME A TEAM PLAYS GIVEN A TEAM NAME, OR NO IF THE TEAM DOES NOT PLAY.
    url = "https://api.liquipedia.net/api/v1/match"
    team = team.title()
    params= {'apikey': APIKEY,'wiki': 'counterstrike','limit': 1, 'conditions':'([[date:: >'+today+']] AND [[date:: < '+tomorrow+']]) AND ([[opponent1::'+team+']] OR [[opponent2::'+team+']])'}
    resultresponse = requests.post(url,params)
    jsonman = resultresponse.json()
    jsonman = jsonman.get('result',[])
    if len(jsonman) > 0:
        jsonman = jsonman[0]
        team1 = jsonman.get('opponent1',[])
        team2 = jsonman.get('opponent2',[])
        time1 = jsonman.get('date',[]).split(" ")[1]
        fixedint = int(time1.split(":")[0]) - 6
        if fixedint <= 0:
            fixedint = 24+fixedint
        csttime = datetime.time(fixedint,int(time1.split(":")[1]),int(time1.split(":")[2]))
        return "Yes! "+ team1+ " play against "+ team2+ " at "+ str(csttime) + " CST"
    return "No, "+team+ " do not play today."


