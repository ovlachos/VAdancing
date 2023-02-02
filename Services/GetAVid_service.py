from time import sleep

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.utils import decode as sw_decode

import Logger as logg
from POM import Locators as loc


def getAllVideos(bot):
    bot.mainPage.driver.execute_script("document.body.style.zoom='75%'")
    bot.mainPage.driver.get('https://thebluesroom.com/course-library/')
    sleep(3)
    for topic in loc.TopicLib_XPath:
        sleep(3)
        if bot.mainPage.goToTopic(topic):
            sleep(3)
            bot.mainPage.getListOfAvailableCourses()
            for course in bot.mainPage.courses:
                if bot.mainPage.goToCourse(course):
                    del bot.mainPage.driver.requests
                    sleep(3)
                    videosAlreadyChecked = []
                    if bot.mainPage.getListOfAvailableVideos():
                        names = bot.mainPage.videoNames
                        logg.logSmth(f" Video Names : {names}")
                        while len(videosAlreadyChecked) < len(bot.mainPage.videos):
                            for video in bot.mainPage.videos:
                                videosAlreadyChecked = refreshVideoTree(bot, videosAlreadyChecked)
                                sleep(5)
                                if len(videosAlreadyChecked) % 3 == 0:
                                    bot.mainPage.scroll_FWD()
                                del bot.mainPage.driver.requests
                    bot.mainPage.goBack()


def refreshVideoTree(bot, videosAlreadyChecked):
    sleep(5)
    if bot.mainPage.getListOfAvailableVideos():
        for vid in bot.mainPage.videos:
            currentVidName = vid.accessible_name
            if currentVidName not in videosAlreadyChecked:
                logg.logSmth(f"Current Video Name is {currentVidName}")
                if vid.is_displayed():
                    wait = WebDriverWait(bot.mainPage.driver, 10)
                    vidToClick = wait.until(EC.element_to_be_clickable(vid))
                    vidToClick.click()
                    # vid.click()
                    sleep(5)
                    bot.mainPage.clickOnVidPlayButton()
                    sleep(5)
                    bot.mainPage.driver.refresh()
                    sleep(14)
                    if GaV(bot):
                        videosAlreadyChecked.append(currentVidName)
                else:

                    bot.mainPage.scroll_BWD()
                return videosAlreadyChecked


def GaV(bot):
    all_requests = bot.mainPage.driver.requests
    html_response = getVideoHTML(all_requests)
    if html_response:
        try:
            final_link, title = getFinalMP4Link(html_response)
            logg.logSmth(f"----\ Video title is: {title}")
            logg.logSmth(f"----\ Video link is: {final_link}")
            return True
        except:
            logg.logSmth(f" We have a fail for {html_response}")
            return False


def getFinalMP4Link(htmlResponse):
    commasep = htmlResponse.split(',')
    title = 'nothing to see here'

    for field in commasep:
        if "title\":\"" in field:
            title = field.split('\"')
            try:
                title = title[-2]
            except:
                title = field

    for field in commasep:
        if "vod-pro" in field:
            ind = commasep.index(field)
            try:
                if commasep[(ind + 2)]:
                    if "1080" in commasep[(ind + 2)]:
                        fieldBreakDown = field.split("\"")
                        for item in fieldBreakDown:
                            if 'http' in item:
                                return item, title
                    elif "720" in commasep[(ind + 2)]:
                        fieldBreakDown = field.split("\"")
                        for item in fieldBreakDown:
                            if 'http' in item:
                                return item, title
            except:
                logg.logSmth(f"----\ Video title is: {title}\n")


def getVideoHTML(all_requests):
    allData = []
    for req in all_requests:
        if req.response:
            if 'player.vimeo.com' in req.url:
                data = sw_decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
                data = data.decode("utf8")
                allData.append(data)
    if len(allData) > 1:
        return allData[0]
