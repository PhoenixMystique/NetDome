import glob
import json
import os
import time
import traceback
from datetime import datetime
from instagrapi import Client
from MainPageBot import PageBot
from value import bcolors
from random import randrange
from Scrapster import MegaEngine
import random
import logging

class SharpEngine:
     setting=None
     scrapster=None
     IsRefreshSessionData=False
     botpass=""
     botuser=""
     MainBot=""
     AMOUNT=None
     DELAY=None
     CAPTION=None
     SCRAPAMOUNT=None
     POSTDELAY=None
     AMOUNT=None
     RESTARTDELAY=None
     logger=None

     client=None
     def  __init__(self,setting,clint,logger):
        self.setting=setting
        self.client=clint
        self.logger=logger
        self.DELAY= randrange(self.setting["Delay"][0],self.setting["Delay"][1])
        print(bcolors.OKGREEN + "[LOGGEDIN] WAIT FOR " + str((9 * self.DELAY)) + bcolors.ENDC)
        self.CAPTION=self.setting["Caption"]
        self.SCRAPAMOUNT=randrange(self.setting["ScrapAmount"][0],self.setting["ScrapAmount"][1])
        self.POSTDELAY=randrange(self.setting["PostDelay"][0],self.setting["PostDelay"][1])
        self.AMOUNT=randrange(self.setting["Amount"][0],self.setting["Amount"][1])
        self.RESTARTDELAY=randrange(self.setting["RestartDelay"][0],self.setting["RestartDelay"][1])
        logger.info("Scrapamount = "+str(self.SCRAPAMOUNT)+" Delay ="+str(self.DELAY))
        self.scrapster()
        self.Mainbot()

     def Mainbot(self):
         self.MainBot = PageBot(self.setting["RootUser"][0],
                                self.setting["RootUser"][1],
                                self.DELAY,
                                self.CAPTION,
                                self.client,
                                self.logger,
                                self.setting["DriverPath"]
                                )

     def scrapster(self):

         self.scrapster = MegaEngine(self.setting["bot"][0],
                                     self.setting["bot"][1],
                                     self.setting["DriverPath"],
                                     self.DELAY,self.logger)
         REELS = 0
         IMAGES = 0
         for users in self.setting["Accounts"]:
             self.logger.info("[Fetching_Posts] Currently Fetching @"+users)
             try:
                 Total = self.PostLicker(users,self.SCRAPAMOUNT)
                 REELS += Total[1]
                 IMAGES += Total[0]
             except Exception as e:
                 self.logger.warning("[PostLicker]  " + str(e) +" In "+traceback.format_exc())
             time.sleep(self.DELAY)
             self.scrapster.SaveOldPost()
         self.logger.info("[Successfully_Fetched] Total " + str(
             (REELS + IMAGES)) + " Posts Newly Fetched  STAST : Reels=" + str(REELS) + " Images=" + str(
             IMAGES))
         self.scrapster.close()


     def PostLicker(self,UssersAccount,Amount):
         Total=[0,0]
         if self.scrapster.CheckLogInRequired(self.scrapster.Driver):
             self.scrapster.UpdateSessionoid()
         Posts = self.scrapster.User_Post_Scrapper(UssersAccount,Amount)
         for post in Posts:
             try:
                 Check =  self.scrapster.isVideo(post)
                 if Check==1:
                     Total[1] +=self.scrapster.reelsDownloader(post)
                 elif Check==0:
                     Total[0] += self.scrapster.ImagePostDownlaod(post)
                 else:
                     continue
             except Exception:
                 continue
         return Total


     def Uploader(self,Amount):
         uploaded=0
         Posts = glob.glob(os.getcwd() +  "/Media/Posts/*.png")
         Videos = glob.glob(os.getcwd() + "/Media/Reels/*.mp4")
         lenm=len(Posts) + len(Videos)
         if (lenm)>0:
             Times=0
             if (lenm)>Amount:
                 Times=int((lenm)/Amount)
             if Times == 0:
                 if (lenm) > 0:
                     Times = 1
             if Amount > (lenm):
                 Amount = (lenm)
        
             self.logger.info( "[Upload_Loop] Posting "+str(Amount)+" Posts each in "+str(Times)+"'s" )
             for i in range (Times):
                  try:
                      uploaded+=self.MainBot.Uploader(Amount)
                      self.logger.info("[Break] Posting Stop for " + str(self.POSTDELAY) + " Currently in " + str(i) + "'th Loop" )
                      time.sleep(self.POSTDELAY)
                  except Exception as e:
                       self.logger.info( "[Upload_Loop_Error] Posting "+str(e))
                      
         return  uploaded

     def getRestartDelay(self):

         return self.RESTARTDELAY

     def getAmount(self):
         return self.AMOUNT
     def CurrrentTime(self):
         now = datetime.now()
         return now.strftime("%H:%M:%S")
