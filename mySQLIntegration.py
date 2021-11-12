import mysql.connector
from pyasn1.type import char
import twitchIntegration
import speechRecognitionIntegration
import liquipediaIntegration

lines = []
with open('resources/nadeinsert.txt') as f:
    lines = f.readlines()
f.close()
mydb = mysql.connector.connect(
    host="####################",
    user="#####",
    password="#####",
    database="#####"
)
nadecursor = mydb.cursor(buffered=True)
twitchcursor = mydb.cursor(buffered=True)
tempcursor = mydb.cursor(buffered=True)
transnotifcursor = mydb.cursor(buffered=True)
notifcursor = mydb.cursor(buffered=True)



# COMMAND TO RETURN URL GIVEN A VOICE COMMAND (HOW DO I *NADETYPE* *NADEPOSITION* FROM *NADE_TEAM* ON *NADE_MAP*)
def getNadeURL(input, map, side):
    try:
        input = input.replace("how do i", "")
        input = input.replace("how do you", "")
        # Asigns the nadetype from the string returned.
        if "smoke" in input:
            nadetype = "smoke"
        else:
            if "flash" in input:
                nadetype = "flash"
            else:
                if "nade" in input:
                    nadetype = "nade"
                else:
                    nadetype = "molotov"
        input = input.replace((nadetype + " "), "")
        # Assigns the nadeposition from whats left of the string
        nadeposition = input.replace(" ", "")
        nadecursor.execute(f"SELECT nade_url FROM blu_nades WHERE nade_type = '{nadetype}' AND nade_position = '{nadeposition}' AND nade_map = '{map}' AND nade_team = '{side}'")
        url = nadecursor.fetchall()[0][0]
        if url == None:
            return "Sorry, No Nade Found."
        return url
    except:
        return "Invalid Command!"



# COMMAND RUN TO NOTIFY 
def livenotifs():
    twitchcursor.execute("SELECT * FROM blu_streamers")
    for row in twitchcursor:
        streamer = row[2]
        sqlstatus = row[1].lower()
        twitchstatus = twitchIntegration.streamerstatus(streamer)
        if twitchstatus == 'live':
            if sqlstatus == 'live':
                None
            else:
                tempcursor.execute(f"UPDATE blu_streamers SET streamer_status = 'live' WHERE streamer_name = '{streamer}'")
                mydb.commit()
                speechRecognitionIntegration.streamnotifs(streamer)
                return(streamer + " is Live! Do you want to watch?")
        else:
            tempcursor.execute(f"UPDATE blu_streamers SET streamer_status = 'notlive' WHERE streamer_name = '{streamer}'")
            mydb.commit()


#Stores transfer notifications in the notifications table.
def storeTransferNotifications():
    transfers = liquipediaIntegration.checktransfers()
    token = ""
    for transfer in transfers:
        # NORMALIZES INPUT
        transfer = transfer.split(',')
        player = transfer[0]
        team1 = transfer[1]
        if team1 == "":
            team1 = "None"
        team2 = transfer[2]
        if team2 == "":
            team2 = "None"
        token = f"{list(player)[0]}{list(team1)[0]}{list(team2)[0]}"

        transnotifcursor.execute(f"SELECT COUNT(*) FROM notifications WHERE token = '{token}'")
        if transnotifcursor.fetchall()[0][0] == 0:
            transnotifcursor.execute(f"INSERT INTO notifications(token,notificationtext) VALUES('{token}','{makeTransferText(player,team1,team2)}')")
        mydb.commit()


#makes the text that is stored in the notifications table
def makeTransferText(player,team1,team2):
    if team1=="None":
        return f"{player} has been signed by {team2}"
    if team2=="None":
        return f"{player} has been cut by {team1}"
    return f"{player} has moved from {team1} to {team2}"
 


def transNotifications():
    storeTransferNotifications()
    notifcursor.execute(f"SELECT COUNT(*) FROM notifications")
    notificationnumber = notifcursor.fetchall()[0][0]
    ans = []
    if notificationnumber == 0:
        return "No Notifications for today!"
    else:
        notifcursor.execute(f"SELECT notificationtext FROM notifications")
        #print(notifcursor.fetchall()[0][0])
        for row in notifcursor.fetchall():
            ans.append(row[0])
            tempcursor.execute(f"DELETE FROM notifications WHERE notificationtext = '{row[0]}'")
            mydb.commit()
        ans.append("That's all the transfers for today!")
        return ans


def availableNades(map, side):
    nades = []
    temp = []
    nadecursor.execute(f"SELECT nade_type, nade_position FROM blu_nades WHERE nade_team = '{side}' and nade_map = '{map}'")
    for row in nadecursor:
        temp = row[0] + " " + row[1]
        nades.append(temp)
    return nades


def storeNades():
    resetfile = lines[0:13]
    count = 0
    del lines[0:13]
    for row in lines:
        row = row.split(",")
        nadecursor.execute(f"INSERT INTO blu_nades(nade_type,nade_position,nade_team,nade_map,nade_url) VALUES ('{row[0]}','{row[1]}','{row[2]}','{row[3]}', '{row[4]}');")
        count = count + 1
    f = open("resources/nadeinsert.txt", "w")
    for row in resetfile:
        f.write(row)
    f.close()
    f = open("resources/nadeinsert.txt", "r")
    mydb.commit()
    return str(count) + " nades have been inserted into the collection!"