from selenium.webdriver import Keys

from POM import Locators as loc
from time import sleep
from seleniumwire.utils import decode as sw_decode


def GaV(bot, url):
    bot.mainPage.driver.get(url)
    sleep(4)
    bot.mainPage.driver.refresh()
    all_requests = bot.mainPage.driver.requests
    html_response = getVideoHTML(all_requests)
    if html_response:
        final_link, title = getFinalMP4Link(html_response)
        print(final_link)
        print(title)

        # try to download
        # bot.mainPage.driver.get(final_link)
        # elem = bot.mainPage.page.getPageElement_tryHard('//div[contains(text(),' ')]')
        # elem.send_keys(Keys.COMMAND, "s")


def getFinalMP4Link(htmlResponse):
    commasep = htmlResponse.split(',')

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
            except:
                pass


def getVideoHTML(all_requests):
    for req in all_requests:
        if req.response:
            if 'player.vimeo.com' in req.url:
                data = sw_decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
                data = data.decode("utf8")
                return data
