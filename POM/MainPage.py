from time import sleep
from POM import Locators as loc


class MainPage:
    def __init__(self, webPage):
        # from POM import insta_topRibbon_POM as topRibbon
        self.page = webPage
        self.driver = self.page.driver
        sleep(1)

    def goToTopic(self, topicName):
        button = self.page.getPageElement_tryHard(loc.courseCategory_XPath.get(topicName))
        if button:
            button.click()
            return True

    def getListOfAvailableCourses(self):
        self.courses = self.page.getPageElements_tryHard(loc.courseCategory_XPath.get('startCourseButtons'))
        if self.courses:
            self.courseNames = []
            for course in self.courses:
                self.courseNames.append(course.text)
                return True

    def goToCourse(self, courseName):
        if self.courses:
            for course in self.courses:
                if courseName in course.text:
                    course.click()
                    return True

    def getListOfAvailableVideos(self):
        self.videos = self.page.getPageElements_tryHard(loc.courseCategory_XPath.get('videoThumbs'))
        if self.videos:
            return True
