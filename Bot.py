import auth
from random import randint
from time import sleep
#
from Services import GetAVid_service as GAV
from POM import webPage as wp
from POM import logIn_page as login
from POM import Locators as loc


class InstaBot:
    datetimeStringFormat_day = '%Y_%m_%d'

    def __init__(self, headless=False):
        # self.fileHandler = fh.FileHandlerBot()
        # self.memoryManager = UserMemoryManager.UserMemoryManager()
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

        # List vars
        # self.targetHashtags_frame = self.fileHandler.CSV_getFrameFromCSVfile('hashtagsToLookForCSV')
        # self.targetHashtags_List = self.targetHashtags_frame[self.targetHashtags_frame.columns[0]].tolist()
        # self.words_frame = self.fileHandler.CSV_getFrameFromCSVfile('wordsToLookForInBioCSV')
        # self.words = self.words_frame[self.words_frame.columns[0]].tolist()

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

    def delayOps(self, minimum=2, maximum=20):
        sleepTime = randint((minimum * 60), (maximum * 60))
        print(f'Sleeping for {int(sleepTime / 60)} minutes')
        sleep(sleepTime)

    def getAvideo(self):
        self.mainPage.driver.get('https://thebluesroom.com/course-library/')
        for elem in loc.courseLib_XPath:

            category_page = self.navigateToCourseCategory(elem)
            if category_page:
                allCourseElements = self.webPage.getPageElements_tryHard(loc.courseCategory_XPath.get('startCourseButtons'))
                if len(allCourseElements) > 0:
                    for course in allCourseElements:

                        coursePage = self.navigateToCourse(course)
                        if coursePage:

                            allCourseTumbs = self.webPage.getPageElements_tryHard(loc.courseVideos_XPath.get('videoThumbs'))
                            if len(allCourseTumbs) > 0:
                                for thumb in allCourseTumbs:
                                    self.navigateToVideo(thumb)
                                    # GAV.GaV('som')
                                self.webPage.driver.back()  # back to courses
                            self.webPage.driver.back()  # back to categories
                        # self.webPage.driver.back()  # back to top page

        # return GAV.GaV(self, "vidURL")

    def navigateToCourseCategory(self, key):
        sleep(2)
        elementTOClick = self.mainPage.page.getPageElement_tryHard(loc.courseLib_XPath.get(key))
        if elementTOClick:
            elementTOClick.click()
            return elementTOClick

    def navigateToCourse(self, course):
        course.click()
        return course

    def navigateToVideo(self, thumb):
        thumb.click()
        return thumb
