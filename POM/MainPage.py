from time import sleep

from selenium.webdriver import ActionChains, Keys

import Logger as logg
from POM import Locators as loc


class ItemVideo:
    def __init__(self, webPage, webElem):
        self.name = ''
        self.url = ''
        self.webElement = webElem
        self.page = webPage


class Course(ItemVideo):
    pass


class Topic(ItemVideo):
    pass


class Video(ItemVideo):
    pass


class MainPage:
    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

        sleep(1)

    def navigateToCourseLibrary(self):
        ribbonButton = self.page.getPageElement_tryHard(loc.homePage_XPath.get('courses'))
        if ribbonButton:
            ribbonButton.click()

    def getListOfAvailableVideos(self):
        self.videos = []

        self.videoWebElements = self.page.getPageElements_tryHard(loc.courseVideos_XPath.get('videoThumbs'))
        self.videoThumbsToClick = self.page.getPageElements_tryHard(loc.courseVideos_XPath.get('videoThumbsToClick'))

        if self.videoWebElements:

            p = 0
            for videoElement in self.videoWebElements:
                video = Video(self.page, videoElement)
                video.name = videoElement.accessible_name
                video.url = self.videoThumbsToClick[p].get_attribute('href')

                self.videos.append(video)
                logg.logSmth(f"{p}-{video.name}-{video.url}")

                p += 1

            return True

    def getListOfAvailableCourses(self):
        self.courses = []
        self.courseTruenames = []

        self.courseWebElements = self.page.getPageElements_tryHard(loc.courseCategory_XPath.get('startCourseButtons'))
        self.courseTruenames = self.page.getPageElements_tryHard(loc.courseCategory_XPath.get('courseName'))

        if self.courseWebElements:

            p = 0
            for courseWebElem in self.courseWebElements:
                course = Course(self.page, courseWebElem)
                course.url = courseWebElem.get_attribute('href')

                try:
                    course.name = course.url.split("/")[-2]
                except:
                    try:
                        course.name = self.courseTruenames[p].accessible_name
                    except:
                        continue

                testList = [c for c in self.courses if course.url in c.url]
                if len(testList) == 0:
                    self.courses.append(course)
                    logg.logSmth(f"Course Name: {course.name} ->  {course.url} ")

                p += 1

            return True

    def goToCourse_Name(self, courseName):
        if self.courses:
            for course in self.courses:
                if courseName in course.name:
                    if course.url:
                        self.driver.get(course.url)
                        return True

    def goToCourse(self, course):
        if self.courses:
            if course in self.courses:
                if course.url:
                    try:
                        self.driver.get(course.url)
                        return True
                    except:
                        return

    def goToVideo(self, vid):
        if self.videos:
            if vid in self.videos:
                if vid.url:
                    try:
                        self.driver.get(vid.url)
                    except Exception as e:
                        if 'renderer' in str(e):
                            self.driver.execute_script("window.stop();")
                    finally:
                        return True

    def refreshVideo(self):
        try:
            self.driver.refresh()
        except Exception as e:
            if 'renderer' in str(e):
                self.driver.execute_script("window.stop();")
        finally:
            return True

    # You can Only navigate to a topic by clicking on the button.
    # There is no unique URL for any topic, thus navigating by URL is impossible
    def goToTopic(self, topicName):
        button = self.page.getPageElement_tryHard(loc.TopicLib_XPath.get(topicName), True)
        if button:
            button.click()
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
            # self.driver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            self.driver.execute_script("window.scrollTo(0, 150)")
            button = self.page.getPageElement_tryHard(loc.courseVideos_XPath.get('playButton'))
            if button:
                actions = ActionChains(self.driver)
                actions.move_to_element(button).perform()
                button.click()
            else:
                logg.logSmth("Play button click failed")
        except:
            logg.logSmth("Play button click failed")
