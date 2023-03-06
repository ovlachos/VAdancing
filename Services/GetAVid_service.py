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
                        if bot.mainPage.getListOfAvailableVideos(verbose=True):

                            for vid in bot.mainPage.videos:
                                logg.logSmth(f"----/ Video Name is: {vid.name}")
                                logg.logSmth(f"----/ Video URL is: {vid.url}")

            bot.mainPage.driver.get('https://thebluesroom.com/course-library/')


def getAllVideos(bot):
    logg.logSmth('\n')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')

    try:
        bot.mainPage.navigateToCourseLibrary()
    except Exception as e:
        sleep(3)
        if 'renderer' in str(e):
            bot.mainPage.driver.execute_script("window.stop();")

    sleep(3)
    for topic in loc.TopicLib_XPath:
        logg.logSmth(f"\n\n")
        logg.logSmth(f"Topic is {topic}")
        logg.logSmth(f"*******************************************")

        if bot.mainPage.goToTopic(topic):
            sleep(3)

            if bot.mainPage.getListOfAvailableCourses(verbose=True):
                for course in bot.mainPage.courses:
                    logg.logSmth(f"\n")
                    logg.logSmth(f"--/ Course Name is: {course.name}")
                    logg.logSmth(f"--/ Course URL is: {course.url}")
                    logg.logSmth(f"*******************************************")

                    if bot.mainPage.goToCourse(course):
                        sleep(4)

                        videosAlreadyChecked = []
                        if bot.mainPage.getListOfAvailableVideos():
                            vidCounter = 0
                            for vid in bot.mainPage.videos:
                                logg.logSmth(f"----/ Expected Video Name is: {vidCounter}-{vid.name}")
                                vidCounter += 1

                                del bot.mainPage.driver.requests
                                if bot.mainPage.goToVideo(vid):
                                    sleep(3)
                                    videosAlreadyChecked = refreshVideoTree(bot, videosAlreadyChecked, vid.name)
                                    sleep(5)
                                    del bot.mainPage.driver.requests

            bot.mainPage.driver.get('https://thebluesroom.com/course-library/')


def getAVideo(bot, vidURL):
    logg.logSmth('\n')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    videosAlreadyChecked = []
    bot.mainPage.driver.get(vidURL)

    del bot.mainPage.driver.requests

    sleep(3)
    videosAlreadyChecked = refreshVideoTree(bot, videosAlreadyChecked, 'vid.name')
    sleep(5)


def getACourse(bot, courseUrl):
    # https://thebluesroom.com/course-library/hip-action/
    logg.logSmth('\n')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')
    logg.logSmth('|||||||******************************************|||||||')

    bot.mainPage.driver.get(courseUrl)
    # bot.mainPage.navigateToCourseLibrary()
    if bot.mainPage.getListOfAvailableVideos(verbose=True):
        videosAlreadyChecked = []
        vidCounter = 0

        for vid in bot.mainPage.videos:
            logg.logSmth(f"----/ Expected Video Name is: {vidCounter}-{vid.name}")
            vidCounter += 1

            while len(videosAlreadyChecked) != vidCounter:
                sleep(3)
                videosAlreadyChecked = refreshVideoTree(bot, videosAlreadyChecked, vid.name)
                sleep(5)
                del bot.mainPage.driver.requests

            bot.mainPage.goToNextVideoThumb(vid.url)


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
    # bot.mainPage.clickOnVidPlayButton()
    if GaV(bot):
        logg.logSmth('GaV ok')
    else:
        logg.logSmth('GaV NOT ok')


def refreshVideoTree(bot, videosAlreadyChecked, expectedName=''):
    sleep(5)
    # bot.mainPage.driver.execute_script("window.stop();")

    bot.mainPage.refreshVideo()

    sleep(8)
    # bot.mainPage.driver.execute_script("window.stop();")

    # for i in range(0, 3):
    if GaV(bot, videosAlreadyChecked, expectedName):
        videosAlreadyChecked.append(expectedName)
    else:
        logg.logSmth(f"Refresh video error for {expectedName}")

    logg.logSmth(f"Videos actually checked: {len(videosAlreadyChecked)}")
    return videosAlreadyChecked


def GaV(bot, videosAlreadyChecked, expectedName=' '):
    html_response = getHTMLResponse(bot)

    if not html_response:  # switch_to_frame
        html_response = getHTMLResponse_Alt(bot, html_response)

    if html_response:
        try:
            final_link, title = getFinalMP4Link(html_response)

            nameCheck = htmlResponseNameCheck(expectedName, title, videosAlreadyChecked)
            if not nameCheck:
                return False

            if not final_link:
                logg.logSmth("No final link Response")
                return False

            if final_link:
                logg.logSmth(f"----\ Video title is: {title}")
                logg.logSmth(f"----\ Video link is: {final_link}")
                return True
        except Exception as e:
            logg.logSmth(f" We have a fail for {expectedName}. Exception is \n\t\t {e}")
            return False


def htmlResponseNameCheck(expectedName, title, videosAlreadyChecked):
    nameLength = len(expectedName) - 3
    if expectedName[-nameLength:] not in title:
        logg.logSmth(f"Expected: {expectedName}\nGot: {title}")
        for name in videosAlreadyChecked:
            if title in name:
                return True
        return False
    return True


def getHTMLResponse_Alt(bot, html_response):
    # src = bot.mainPage.page.getPageElements_tryHard(loc.courseVideos_XPath.get('videoFrame'))
    iFrameWebElement = bot.mainPage.getVideoWebElement()
    bot.mainPage.driver.switch_to.frame(iFrameWebElement)
    src = bot.mainPage.driver.page_source
    bot.mainPage.driver.switch_to.default_content()
    if src:
        html_response = src
    else:
        logg.logSmth("No HTML Response - tried backup")
    return html_response


def getHTMLResponse(bot):
    all_requests = bot.mainPage.driver.requests
    if not all_requests:
        logg.logSmth("No Requests")
    html_response = getVideoHTML(all_requests)
    return html_response


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
                    # logg.logSmth(f"Resolution: {commasep[(ind + 2)]}")
                    if "1080" in commasep[(ind + 2)]:
                        fieldBreakDown = field.split("\"")
                        for item in fieldBreakDown:
                            if 'http' in item:
                                # logg.logSmth('1080p version')
                                return item, title  # RETURN
                    elif "720" in commasep[(ind + 2)]:
                        fieldBreakDown = field.split("\"")
                        for item in fieldBreakDown:
                            if 'http' in item:
                                # logg.logSmth('720p version')
                                return item, title  # RETURN
                    else:
                        pass
                        # logg.logSmth("Final MP4 link could not be extracted from HTML response")
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
