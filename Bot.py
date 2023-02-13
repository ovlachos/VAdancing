from random import randint
from time import sleep

import auth
from POM import logIn_page as login
from POM import webPage as wp
from Services import GetAVid_service as GAV


class InstaBot:
    datetimeStringFormat_day = '%Y_%m_%d'

    def __init__(self, headless=False):
        self.headless = headless
        self.timeUpperBound = 48
        self.timeLowerBound = 34
        self.timeLimitSinceLastLoved = 30
        self.followMana = 100
        self.followManaMax = 100
        self.getBrowser()

        # Game vars
        self.daysBeforeIunFollow = 14 - 1
        self.daysBeforeIunLove = self.daysBeforeIunFollow + 5

    def logIn(self):
        logInPage = login.VA_LogIn(self.webPage)
        self.mainPage = logInPage.logIn(auth.username, auth.password)

    def logOut(self):
        self.mainPage.topRibbon_myAccount.logOut()

    def shutDown(self):
        self.logOut()
        sleep(1)
        self.webPage.instance.writeSessionDataToJSON()
        self.webPage.killBrowser()

    def getBrowser(self):
        self.webPage = wp.WebPage(self.headless)

    def botSleep(self, factor=1):
        sleep(randint(factor * self.timeLowerBound, factor * self.timeUpperBound))

    def getAvideo(self):
        return GAV.getAllVideos(self)

    def getAvideoAssisted(self):
        # return GAV.userAssistedVideoGetWindows(self)
        return GAV.userAssistedVideoGetMacOS(self)