from time import sleep

from POM import Locators as loc


class MainPage:
    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver
        self.courseDict = {}
        sleep(1)

    def goToTopic(self, topicName):
        button = self.page.getPageElement_tryHard(loc.TopicLib_XPath.get(topicName))
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

            print(self.courseDict)
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
                print(f"--\ {self.courseDict.get(course.accessible_name)}")
                course.click()
                return True

    def getListOfAvailableVideos(self):
        self.videos = self.page.getPageElements_tryHard(loc.courseVideos_XPath.get('videoThumbs'))
        self.videoNames = []
        if self.videos:
            for video in self.videos:
                self.videoNames.append(video.accessible_name)
            return True

    def scroll_BWD(self):
        button = self.page.getPageElement_tryHard(loc.courseVideos_XPath.get('swiperNext'))
        if button:
            button.click()

    def scroll_FWD(self):
        button = self.page.getPageElement_tryHard(loc.courseVideos_XPath.get('swiperPrev'))
        if button:
            button.click()
