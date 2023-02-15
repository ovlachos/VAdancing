# from getch import getch
from time import sleep

import keyboard
from seleniumwire.utils import decode as sw_decode

import Logger as logg
from POM import Locators as loc


# Another Idea would be to get all the video carousel links that end in the
# form of "...vimeography_video=" plus some random number
# Write a function that harvests all these links in to a .json file organised by class and video title in a catalogue.

# If the title of the video provided by the HTML response is not the one expected e.g. "top tips dancing between the beats"
# I need to go to the next video and then go back again to get the right video ----\ Video title is: Top Tip: Dancing between the beats

# I need to create a list containing [videoURL, videoName] tuples

def harvestVideoLinks(bot):
    logg.logSmth('\n')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    bot.mainPage.driver.get('https://thebluesroom.com/course-library/')
    sleep(3)
    for topic in loc.TopicLib_XPath:
        logg.logSmth(f"\n\n")
        logg.logSmth(f"Topic is {topic}")
        logg.logSmth(f"*******************************************")

        if bot.mainPage.goToTopic(topic):
            sleep(3)

            if bot.mainPage.getListOfAvailableCourses():

                for course in bot.mainPage.courses:
                    logg.logSmth(f"\n")
                    logg.logSmth(f"--/ Course Name is: {course.name}")
                    logg.logSmth(f"--/ Course URL is: {course.url}")
                    logg.logSmth(f"*******************************************")

                    if bot.mainPage.goToCourse(course):
                        sleep(4)

                        videosAlreadyChecked = []
                        if bot.mainPage.getListOfAvailableVideos():

                            for vid in bot.mainPage.videos:
                                logg.logSmth(f"----/ Video Name is: {vid.name}")
                                logg.logSmth(f"----/ Video URL is: {vid.url}")

            bot.mainPage.driver.get('https://thebluesroom.com/course-library/')


def getAllVideos(bot):
    logg.logSmth('\n')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    bot.mainPage.driver.get('https://thebluesroom.com/course-library/')
    sleep(3)
    for topic in loc.TopicLib_XPath:
        logg.logSmth(f"\n\n")
        logg.logSmth(f"Topic is {topic}")
        logg.logSmth(f"*******************************************")

        if bot.mainPage.goToTopic(topic):
            sleep(3)

            if bot.mainPage.getListOfAvailableCourses():
                for course in bot.mainPage.courses:
                    logg.logSmth(f"\n")
                    logg.logSmth(f"--/ Course Name is: {course.name}")
                    logg.logSmth(f"--/ Course URL is: {course.url}")
                    logg.logSmth(f"*******************************************")

                    if bot.mainPage.goToCourse(course):
                        sleep(4)

                        videosAlreadyChecked = []
                        if bot.mainPage.getListOfAvailableVideos():

                            for vid in bot.mainPage.videos:
                                logg.logSmth(f"----/ Video Name is: {vid.name}")
                                logg.logSmth(f"----/ Video URL is: {vid.url}")

                                del bot.mainPage.driver.requests
                                if bot.mainPage.goToVideo(vid):
                                    sleep(3)
                                    videosAlreadyChecked = refreshVideoTree(bot, videosAlreadyChecked, vid.name)
                                    sleep(5)
                                    del bot.mainPage.driver.requests

            bot.mainPage.driver.get('https://thebluesroom.com/course-library/')


def userAssistedVideoGetWindows(bot):
    bot.mainPage.driver.get('https://thebluesroom.com/course-library/')
    sleep(3)

    for i in range(0, 35):
        logg.logSmth(f"Waiting on q key press for the {i} time")
        while True:
            # I navigate manually and press the key to get the data, then wait again for key press
            if keyboard.is_pressed("q"):
                if bot.mainPage.getListOfAvailableVideos():
                    for vid in bot.mainPage.videoWebElements:
                        pass
                        # logg.logSmth(bot.mainPage.videoNames)
                        # logg.logSmth(bot.mainPage.videoThumbsToClick)
                del bot.mainPage.driver.requests
                sleep(2)
                refreshVideoTreeSimple(bot)
                del bot.mainPage.driver.requests
                break


def userAssistedVideoGetMacOS(bot):
    bot.mainPage.driver.get('https://thebluesroom.com/course-library/')
    sleep(3)

    for i in range(0, 35):
        logg.logSmth(f"Waiting on 'q' key press for the {i} time")
        while True:
            # I navigate manually and press the key to get the data, then wait again for key press

            char = 'getch()  # read the pressed key'
            if char == chr(113):  # 113 == 'q' print(ord('q')) => 113
                if bot.mainPage.getListOfAvailableVideos():
                    for vid in bot.mainPage.videoWebElements:
                        pass
                del bot.mainPage.driver.requests
                sleep(2)
                refreshVideoTreeSimple(bot)
                del bot.mainPage.driver.requests
                break


def refreshVideoTreeSimple(bot):
    bot.mainPage.driver.refresh()
    sleep(5)
    bot.mainPage.clickOnVidPlayButton()
    if GaV(bot):
        logg.logSmth('GaV ok')
    else:
        logg.logSmth('GaV NOT ok')


def refreshVideoTree(bot, videosAlreadyChecked, expectedName=''):
    sleep(5)
    bot.mainPage.clickOnVidPlayButton()
    sleep(5)
    bot.mainPage.driver.refresh()
    sleep(14)
    for i in range(0, 5):
        if GaV(bot, expectedName):
            videosAlreadyChecked.append(expectedName)
        else:
            logg.logSmth(f"Refresh video error for {expectedName}")

    return videosAlreadyChecked


def makeSureWeAreGettingTheRightVideoRequests(bot, vid):
    # Refresh
    del bot.mainPage.driver.requests
    bot.mainPage.driver.refresh()
    del bot.mainPage.driver.requests

    # Go to next/previous video
    targetVidIndex = bot.mainPage.videoThumbsToClick.index(vid)
    if len(bot.mainPage.videoThumbsToClick) > targetVidIndex:
        nextVid = bot.mainPage.videoThumbsToClick[(targetVidIndex + 1)]
    else:
        nextVid = bot.mainPage.videoThumbsToClick[(targetVidIndex + -1)]

        # navigate to next/prev video URL

    # Wait
    sleep(5)

    # Go back to target video
    # navigate to target video URL

    # Refresh
    bot.mainPage.driver.refresh()


def GaV(bot, expectedName=' '):
    all_requests = bot.mainPage.driver.requests
    if not all_requests:
        logg.logSmth("No Requests")

    html_response = getVideoHTML(all_requests)
    if not html_response:
        logg.logSmth("No HTML Response")

    if html_response:
        try:
            final_link, title = getFinalMP4Link(html_response)
            if expectedName in title:
                logg.logSmth(f"----\ Video title is: {title}")
                logg.logSmth(f"----\ Video link is: {final_link}")
                return True
            else:
                logg.logSmth(f"----\ Video title is not the expected")
                logg.logSmth(f"----\ Video title is: {title}")
                logg.logSmth(f"----\ Video link is: {final_link}")
                return False
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
                                return item, title  # RETURN
                    elif "720" in commasep[(ind + 2)]:
                        fieldBreakDown = field.split("\"")
                        for item in fieldBreakDown:
                            if 'http' in item:
                                return item, title  # RETURN
                    else:
                        logg.logSmth("Final MP4 link could not be extracted from HTML response")
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
