
import traceback
import glob
import json
import random
from pymediainfo import MediaInfo
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

import os

from Scrapster import MegaEngine
from value import bcolors

import subprocess



class PageBot:
    Username = ""
    Password = ""
    DriverPath = ""
    Drver=None
    Delay=None
    Header=None
    Caption=None
    client=None
    logger=None
    def __init__(self,Username,Password,Delay,Caption,client,logger,driverPath):
        self.Username = Username
        self.Password = Password
        self.client=client
        self.Delay=Delay
        self.loadHeader()
        self.Caption=Caption
        self.logger=logger
        subprocess.run(["killall", "chrome"])
        options = Options()
        options.add_argument("user-data-dir=" + os.getcwd() + "/ChromeProfiles/profile2/")
        # options.add_argument("user-data-dir="+"/home/itz_adi/.config/google-chrome")
        # options.add_argument("--profile-directory=Default")
        options.add_argument("window-size=1980,1080")
        options.add_argument('disable-gpu')
        options.add_argument("--disable-extensions")
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")
        options.add_argument("user-agent=" + self.Header["User-Agent"])
        options.add_argument('--disable-dev-shm-usage')
        self.Driver = webdriver.Chrome(driverPath, options=options)
        self.LogInManager()


    def loadHeader(self):
        with open('jsonfiles/cookies.json', 'r') as sessionfile:
            json_object = json.load(sessionfile)
        sessionfile.close()
        self.Header=json_object
    def DoSomeDelay(self):
        time.sleep(self.Delay)

    def Uploader(self, Amount):
        completed=0
        for i in range (Amount):
          Posts = glob.glob(os.getcwd() + "/Media/Posts/*.png")
          Videos = glob.glob(os.getcwd() + "/Media/Reels/*.mp4")
          if len(Posts)>0 and len(Videos)>0:
              if random.choice([0,1])==0:
                  try:
                      completed +=self.ImageInspector(Posts[0])
                      os.remove(Posts[0])
                  except:
                      continue

              else:
                          completed +=self.VideoInspector(Videos[0])
                          os.remove(Videos[0])
          elif(len(Posts)) > 0:
              completed +=self.ImageInspector(Posts[0])
              os.remove(Posts[0])
          elif (len(Videos)) > 0:
              completed +=self.VideoInspector(Videos[0])
              os.remove(Videos[0])
          time.sleep(100)    
        self.logger.info("[Uploaded_Status_Loop] Total "+str(completed)+" Post Uploade Completed")
        return completed
    def mediaInfo(self,Path):
        media_info = MediaInfo.parse(Path)
        data = {
            "dimension": [],
            "size": None,
            "duration": None

        }
        for track in media_info.tracks:
            if track.track_type == 'Video':
                data["dimension"].append(track.width)
                data["dimension"].append(track.height)
                data["size"] = track.to_data()['stream_size'] / 1000
                data["duration"] = track.to_data()['duration'] / 1000
            if track.track_type == 'Image':
                data["dimension"].append(track.width)
                data["dimension"].append(track.height)
                data["size"] = track.to_data()['stream_size'] / 1000
        return data
    def LogInManager(self):
        loginmanager = MegaEngine(None,None,None,self.Delay,self.logger)
        if loginmanager.CheckLogInRequired(Driver=self.Driver):
            loginmanager.loginUser(self.Username,self.Password,self.Driver)
            loginmanager.initiapopup(True,self.Driver)

    def ImageInspector(self,Path):
        try:
            mediainfo = self.mediaInfo(Path)
            if mediainfo["size"] > 10 and mediainfo["dimension"][0] > 900 and mediainfo["dimension"][1] > 900:
                cap=self.CaptionGenerator(self.Caption)
                uploaded =self.client.photo_upload(path=Path,caption=cap)
                self.logger.info("[IMAGE_Uploaded] With Caption"+cap)
                print(bcolors.OKGREEN + "[IMAGE]Uploaded Successfully" + bcolors.ENDC)
                return 1
            else:
                self.logger.info("[IMAGE_Uploaded_Error] Not Eligible")
                return 0
                
        except Exception as e:
            self.logger.info("[IMAGE_Error] "+str(e)+traceback.format_exc())
            return 0


    def VideoInspector(self,Path):
        try:
            cap = self.CaptionGenerator(self.Caption)
            mediainfo = self.mediaInfo(Path)
            if mediainfo["size"] > 200:
                if mediainfo["duration"] < 60:
                    if mediainfo["dimension"][0] < 1080 and mediainfo["dimension"][1] < 1080:

                        self.client.video_upload(path=Path, caption =cap)

                        print(bcolors.OKGREEN + "[Video]Uploaded Successfully"  + bcolors.ENDC)
                        return 1
                    else:

                        self.client.clip_upload(path=Path, caption =cap)
                        print(bcolors.OKGREEN + "[Reels]Uploaded Successfully" + bcolors.ENDC)
                        return 1

                else:
                    self.client.igtv_upload(title="Sarcasticpunks",path=Path, caption = cap)
                    print(bcolors.OKGREEN + "[IG_TV]Uploaded Successfully"  + bcolors.ENDC)
                    return 1
            else:
                self.logger.info("[Video_Not_Eligibele] ")
                return 0
        except Exception as e:
            self.logger.info("[Video_Error] " + str(e) + traceback.format_exc())
            return 0

    def CaptionGenerator(self,Tags):
        Symbol =random.choice(Tags["Symbols"])
        caption=random.choice(Tags["TagLines"])+"\n"
        for i in range (Tags["Gap"]):
              caption+=Symbol+"\n"
        for tags in range(random.randrange(6,9)):
            caption +=str(self.Radomize(caption,Tags["PreciousTags"]))
        for tags in range (random.randrange(10,15)):
            caption +=str(self.Radomize(caption,Tags["Tags"]))
        return caption
    def Radomize(self,Caption,Tag):
            put = random.choice(Tag)

            if str(Caption).find(put)>0:
                self.Radomize(Caption,Tag)
            return put+" "

    def close(self):
        self.Driver.close()










