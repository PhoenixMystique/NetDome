
from instascrape import *
import json as json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import subprocess
from instascrape import Reel
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
import wget


from value import bcolors


class MegaEngine:
    REELSCOUNT =1
    IMAGECOUNT=1
    Username=None
    Password=None
    DriverPath=None
    Driver=None
    Header=None
    oldpost=None
    DELAY=None
    IGTV=1
    logger=None

    def __init__(self,Username,Password,driverPath,DELAY,logger):
        self.Username=Username
        self.Password=Password
        self.DELAY = DELAY
        self.logger=logger
        if Username != None:
            self.loadHeader()
            subprocess.run(["killall", "chrome"])
            options = Options()
            options.add_argument("user-data-dir=" + os.getcwd() + "/ChromeProfiles/profile1/")
            # options.add_argument("user-data-dir="+"/home/itz_adi/.config/google-chrome")
            # options.add_argument("--profile-directory=Default")
            options.add_argument("window-size=1980,1080")
            options.add_argument('disable-gpu')
            options.add_argument("--disable-extensions")
            options.add_argument('--no-sandbox')
            options.add_argument("--headless")
            options.add_argument("user-agent="+self.Header["User-Agent"])
            options.add_argument('--disable-dev-shm-usage')
            self.Driver = webdriver.Chrome(driverPath,options=options)
            self.loadoldpost()


    def loadoldpost(self):
        with open('jsonfiles/databse.Json', 'r') as posts:
            self.oldpost = json.load(posts)
        posts.close()

    def Closedriver(self):
        self.Driver.close()
    def loadHeader(self):
        with open('jsonfiles/cookies.json', 'r') as sessionfile:
            json_object = json.load(sessionfile)
        sessionfile.close()
        self.Header=json_object

    def get_Driver(self):
        return self.Driver

    def loginUser(self,User,Pass,Driver):
        self.logger.info("[Logg_Not_Detected] Login Started with " + User)
        print("\n" + bcolors.FAIL + "[Logg_Not_Detected] Login Started with " + User+ bcolors.ENDC + "\n")
        try:
            username = WebDriverWait(Driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            self.DoSomeDelay()
            password = WebDriverWait(Driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            self.DoSomeDelay()
        except Exception as e:
            self.loginUser(User,Pass,Driver)
        username.clear()
        username.send_keys(User)
        password.clear()
        password.send_keys(Pass)
        WebDriverWait(Driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        self.DoSomeDelay()
        self.logger.info("[Sucessfully_Logged_In] Logged In with " + User)



    def initiapopup(self,issaveinfo,Driver):
        try:
            if issaveinfo:
                WebDriverWait(Driver, 8).until(EC.element_to_be_clickable((By.XPATH, ' // button[contains(text(), "Save Info")]'))).click()
                self.DoSomeDelay()
            else:
                WebDriverWait(Driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, ' // button[contains(text(), "Not Now")]'))).click()
            WebDriverWait(Driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, ' // button[contains(text(), "Not Now")]'))).click()
        except Exception as e:
            self.DoSomeDelay()

    def UpdateSessionoid(self):
        Driver =self.Driver
        self.loginUser(self.Username,self.Password,Driver)
        self.initiapopup(True,Driver)
        sessionid= Driver.get_cookies()
        userAgent= Driver.execute_script("return navigator.userAgent")
        SESSIONID  =""

        if str(sessionid[1]["value"]).find("/")<0 and str(sessionid[1]["value"]).find("\\")<0:
            SESSIONID=str(sessionid[1]["value"])
            print(SESSIONID)
        elif str(sessionid[2]["value"]).find("/")<0 and str(sessionid[2]["value"]).find("\\")<0:
            SESSIONID = str(sessionid[2]["value"])
            print(SESSIONID)
        elif str(sessionid[3]["value"]).find("/")<0 and str(sessionid[3]["value"]).find("\\")<0:
            SESSIONID = str(sessionid[3]["value"])
            print(SESSIONID)
        elif str(sessionid[4]["value"]).find("/")<0 and str(sessionid[4]["value"]).find("\\")<0:
            SESSIONID = str(sessionid[4]["value"])
            print(SESSIONID)
        elif str(sessionid[5]["value"]).find("/") < 0 and str(sessionid[5]["value"]).find("\\") < 0:
            SESSIONID = str(sessionid[5]["value"]).find("/")
            print(SESSIONID)
        head = {
            "User-Agent": userAgent,
            "cookie": f'sessionid={SESSIONID};'
        }
        with open("jsonfiles/cookies.json", "w") as json_file:
            json.dump(head, json_file)
            self.logger.info("Dumped New Session Header")
            print("Dumped New Session Header")
        json_file.close()
        self.loadHeader()

    def reelsDownloader(self,LinkToreel):
        try:
            reels = Reel(LinkToreel)
            head =self.Header
            reels.scrape(headers=head)
            reels.download(fp = "Media/Reels/reel"+str(self.REELSCOUNT)+".mp4")
            self.REELSCOUNT += 1
            return 1
        except Exception as e:
            print(str(e)+"in line Reels")
            return 0

    def CheckLogInRequired(self,Driver):
        Driver.get("https://www.instagram.com/")
        try:
            WebDriverWait(Driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

            return True

        except Exception as e:
            try: 
              signup=Driver.find_elements_by_tag_name("button")
              for bt in signup:
                if bt.text=="Sign Up":
                    for rm in signup:
                        if rm.text=="Remove Account":
                            rm.click()

                            bhola=Driver.find_elements_by_tag_name("button")
                            for clicks in bhola:
                                  if clicks.text=="Remove":
                                      clicks.click()
                                      return True

            except:
                 return False
            return False




    def DoSomeDelay(self):
        time.sleep(self.DELAY)
    def User_Post_Scrapper(self,AccountName,Amount):
            AccountPost = Profile(AccountName)
            AccountPost.scrape(headers=self.Header)
            self.DoSomeDelay()
            posts = AccountPost.get_posts(self.Driver,Amount)

            PostData =[]
            PostData.extend(self.igtvlicker(AccountName))
            for post in posts:
                PostData.append("https://www.instagram.com/p/"+post.source+"/")
            return PostData
    def igtvlicker(self,Account):
        self.Driver.get("https://www.instagram.com/"+Account+"/channel/")
        time.sleep(self.DELAY)
        links =self.Driver.find_elements_by_tag_name("a")
        collected=0
        LINKS=[]
        for link in links:
            if collected>=self.IGTV:
                break
            if str(link.get_attribute("href")).find("tv")>0:
                LINKS.append(link.get_attribute("href"))
                collected+=1
        return LINKS



    def  isVideo(self,Post):
        if self.isOldPost(Post)==False:
            self.Driver.get(Post)
            self.DoSomeDelay()
            self.PutInOldList(Post)
            try:
                WebDriverWait(self.Driver, 5).until(
                    EC.element_to_be_clickable((By.TAG_NAME, 'video')))
                return 1

            except:

                return 0

        else:

            return 3



    def ImagePostDownlaod(self,ImagePost):
            self.Driver.get(ImagePost)
            img = self.Driver.find_elements_by_tag_name('img')
            img = [i.get_attribute('src') for i in img]
            path = os.getcwd()
            path = os.path.join(path,"Media/Posts")
            save_as = os.path.join(path, "Post"+ str(self.IMAGECOUNT) +
                                       '.png')

            try:
                    wget.download(img[1], save_as)
                    self.IMAGECOUNT += 1
                    return 1
            except Exception as e:
                    print(str(e))
                    return 0


    def isOldPost(self,Link):
        for links in self.oldpost:
            if links == Link:
                return True
        return False

    def PutInOldList(self,posts):
        try:
          self.oldpost.append(posts)
        except Exception as e :
            print(str(e))


    def SaveOldPost(self):
        with open('jsonfiles/databse.Json', 'w') as posts:
            json.dump(self.oldpost, posts)
        posts.close()
    def close(self):
        self.Driver.close()






