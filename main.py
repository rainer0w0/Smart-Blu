import sys
from PyQt5.uic import loadUi
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import speechRecognitionIntegration
import threading
import time

# GUI STUFF I HATE THIS GUI SO MUCH OH MY GOD HOLY GOD
class welcomeScreen(QMainWindow):
    def __init__(self):
        super(welcomeScreen, self).__init__()
        loadUi("blu.ui", self)

    def bluSpeak(self,words):
        if len(words) > 40:
            self.bluTalk.setText(words[:len(words)//2])
            time.sleep(2)
            self.bluTalk.setText(words[len(words)//2:])
        else:
            self.bluTalk.setText(words)
    
    def bluWake(self):
        self.bluSleep.resize(0,0)
        self.bluSpeak("Hello!")
    
    def bluBed(self):
        self.bluSleep.resize(261,241)
        self.bluSpeak("")

app = QApplication(sys.argv)
welcome=welcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(320)
widget.setFixedWidth(480)

def thread1(): # Thread controls all voice input.
    map = "mirage"
    side = "T"
    while True:
        sleep = True
        while sleep:
            sleep = not speechRecognitionIntegration.wake()
        welcome.bluWake()
        listen = True
        while listen:
            welcome.bluWake()
            text = speechRecognitionIntegration.parseMicrophone(side, map)
            print(text)
            listen = False
            if "Map changed to " in text:
                print("Changing map")
                temptext = text.replace("Map changed to ", "")
                map = temptext.replace(" ", "")
                print(map)
            if "Side changed to " in text:
                print("Changing side")
                temptext = text.replace("Side changed to ", "")
                side = temptext.replace(" ", "")
                side = side.upper()
                print(side)
            if text == "Invalid Command!":
                listen = True
            if type(text) == list:
                for row in text:
                    welcome.bluSpeak(row)
                    time.sleep(1)
            else:
                welcome.bluSpeak(text)
                if text == "Invalid Command!":
                    time.sleep(1)
                    welcome.bluSpeak("Please try again")
        time.sleep(3)
        welcome.bluBed()


# THREADING AND MORE GUI STUFF IGNORE THIS :)
t1 = threading.Thread(target=thread1)
t1.start()
widget.show() 
try:
    sys.exit(app.exec())
except:
    print("Exiting")

