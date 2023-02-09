from time import sleep

from selenium.webdriver import ActionChains

import Logger as logg
from POM import Locators as loc


class MainPage:
    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver
        self.courseDict = {}
        sleep(1)

    def goToTopic(self, topicName):
        button = self.page.getPageElement_tryHard(loc.TopicLib_XPath.get(topicName), True)
        if button:
            button.click()
            return True

    def getListOfAvailableCourses(self):
        self.courses = self.page.getPageElements_tryHard(loc.courseCategory_XPath.get('startCourseButtons'))
        self.courseTruenames = self.page.getPageElements_tryHard(loc.courseCategory_XPath.get('courseName'))
        if self.courses:
            self.courseNames = []
            p = 0
            for course in self.courses:
                self.courseNames.append(course.text)
                self.courseDict[course.text] = self.courseTruenames[p].accessible_name
                p += 1

            self.courseNames = [i for i in self.courseNames if i]
            self.courses = [i for i in self.courses if i.text]

            logg.logSmth(self.courseDict)
            return True

    def goToCourse_Name(self, courseName):
        if self.courses:
            for course in self.courses:
                if courseName in course.text:
                    course.click()
                    return True

    def goToCourse(self, course):
        if self.courses:
            if course:
                logg.logSmth(f"--\ {self.courseDict.get(course.accessible_name)}")
                course.click()
                return True

    def getListOfAvailableVideos(self):
        self.videos = self.page.getPageElements_tryHard(loc.courseVideos_XPath.get('videoThumbs'))
        self.videoThumbsToClick = self.page.getPageElements_tryHard(loc.courseVideos_XPath.get('videoThumbsToClick'))
        self.videoNames = []
        if self.videos:
            for video in self.videos:
                self.videoNames.append(video.accessible_name)
            return True

    def scroll_BWD(self):
        try:
            button = self.page.getPageElement_tryHard(loc.courseVideos_XPath.get('swiperPrev'), True)
            if button:
                button.click()
        except:
            logg.logSmth("scroll B failed")

    def scroll_FWD(self):
        try:
            button = self.page.getPageElement_tryHard(loc.courseVideos_XPath.get('swiperNext'), True)
            if button:
                button.click()
        except:
            logg.logSmth("scroll F failed")

    def clickOnVidPlayButton(self):
        try:
            button = self.page.getPageElement_tryHard(loc.courseVideos_XPath.get('playButton'))
            if button:
                actions = ActionChains(self.driver)
                actions.move_to_element(button).perform()
                button.click()
            else:
                logg.logSmth("Play button click failed")
        except:
            logg.logSmth("Play button click failed")
