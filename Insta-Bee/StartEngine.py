import logging
import json
import threading
import time
from datetime import datetime
from instagrapi import Client
from SharpEngine import SharpEngine
from value import bcolors
from random import randrange
SLEEP=False
DELAY=0
SLEEPTIME=0
def Clock():
    global SLEEP,DELAY


    while True:
        now = datetime.now()
        if SLEEPTIME==int(now.strftime("%H")):
            SLEEP=True
            time.sleep(DELAY)
            SLEEP=False
    time.sleep(5)




logging.basicConfig(filename="logs/Sharpster.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
clint =Client()
TotalPost=0
COUNT=0
with open("jsonfiles/Settings.Json", "r") as settings:
    setting = json.load(settings)
Sleep=setting["SleepTime"]
DELAY=Sleep[1]
SLEEPTIME=Sleep[0]
Clock_thread = threading.Thread(target=Clock, name="Clock")
Clock_thread.daemon=True
Clock_thread.start()
clint.login(setting["RootUser"][0],setting["RootUser"][1])
logger.info("Logined Root USER as "+setting["RootUser"][0])
while True:
       Ignite =SharpEngine(setting,clint,logger)
       Uploaded=Ignite.Uploader(Ignite.getAmount())
       TotalPost+=Uploaded
       logger.info( "[COMPLETED] Session Uploads =" +str(Uploaded)+" Total Posts Uploaded ="+str(TotalPost))
       print(bcolors.OKGREEN + "[COMPLETED] Session Uploads =" +str(Uploaded)+" Total Posts Uploaded ="+str(TotalPost) + bcolors.ENDC)
       logger.info("[RESTARTING_IN] "+str(Ignite.getRestartDelay()/3600)+" Hours")
       print(bcolors.OKGREEN+"[RESTARTING_IN] "+str(Ignite.getRestartDelay()/3600)+" Hours"+bcolors.ENDC)
       if SLEEP == True:
           logger.warning(
               "[SLEEPING_MODE]" + "DND U Asshole! Not Gonna Post Anything Before Morning Sleeping RN ")
           while SLEEP:
               time.sleep(800)
               if SLEEP==False:
                   break

           print(bcolors.OKGREEN + "[WAKED_UP] " + str(Ignite.getRestartDelay() / 3600) + " Hours" + bcolors.ENDC)
       else:
           time.sleep(Ignite.getRestartDelay())
           if COUNT%4==0:
              Bigdelay= randrange(setting["BigDelay"][0], setting["BigDelay"][1])
              logger.info(bcolors.WARNING + "[Big_DELAY] " + str(Bigdelay/ 60) + "minutes")
           COUNT+=1
       logger.info("[RESTARTED]"+Ignite.CurrrentTime())
