import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from seleniumwire import webdriver


# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver and a "what page am I currently browsing" method

class Browser:

    def __init__(self, headless=False):

        self.newSession = True

        self.createNewBrowserSession(headless)

    def createNewBrowserSession(self, headless):

        option = webdriver.ChromeOptions()
        option.add_argument('--disable-blink-features=AutomationControlled')
        # option.page_load_strategy = 'eager'
        option.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        option.add_argument("window-size=6000x4000")
        option.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

        self.driver = webdriver.Chrome(options=option)
        self.driver.implicitly_wait(8)
        # self.driver.set_page_load_timeout(30.0)

        executor_url = self.driver.command_executor._url
        session_id = self.driver.session_id

        print(f"New session with:\n\tsession_id: {session_id}\n\texecutor_url: {executor_url}\n")
        self.writeSessionDataToJSON(session_id=session_id, executor_url=executor_url)

    def writeSessionDataToJSON(self, session_id='0', executor_url='0'):
        import json

        sessionData = {}
        sessionData['session_id'] = session_id
        sessionData['executor_url'] = executor_url

        with open('BrowserSession.json', 'w') as json_conf:
            json.dump(sessionData, json_conf)

    def getSessionFromJSON(self):
        import json

        with open('BrowserSession.json', 'r') as json_conf:
            return json.load(json_conf)

    def previousSessionExists(self, dataFromJSON):
        if dataFromJSON['session_id'] == '0':
            return False

        return True

    def clearCache(self):
        return

    # Only needed for Firefox sessions ?
    def create_driver_session(self, session_id, executor_url):
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        new_driver.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        return new_driver


class WebPage:

    def __init__(self, headless=False):
        self.instance = Browser(headless)
        self.driver = self.instance.driver

    def killBrowser(self):
        self.driver.quit()

    def whichPageAmI(self, verbose=False):
        currentPageURL = self.driver.current_url

        if verbose:
            print("Session: {0}\n@ {1}".format(self.driver.session_id, currentPageURL))

        return currentPageURL

    def getPageElement_tryHard(self, xpath, toClick=False):
        attempts = 3
        result = None
        while result is None:
            try:
                result = self.driver.find_element(By.XPATH, xpath)
            except Exception as e:
                attempts -= 1
                sleep(1)
                if attempts == 0:
                    break

        return result

    def getPageElements_tryHard(self, xpath):
        attempts = 3
        results = None
        while results is None:
            try:
                results = self.driver.find_elements(By.XPATH, xpath)
            except Exception as e:
                attempts -= 1
                sleep(1)
                if attempts == 0:
                    break

        return results

    def getAlliFrames(self):
        attempts = 3
        results = None
        while results is None:
            try:
                results = self.driver.find_elements(By.XPATH, '//iframe')
            except Exception as e:
                attempts -= 1
                sleep(1)
                if attempts == 0:
                    break

        return results

    def sendKey(self, key):
        if isinstance(key, str):
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(key)
                actions.perform()
            except Exception as e:
                print(e)

    def slowTypeIntoField(self, fieldXPATH, query):
        try:
            field = self.getPageElement_tryHard(fieldXPATH)
            field.clear()

            for ch in str(query):
                sleep(random.uniform(0, 1))
                field.send_keys(ch)
            sleep(1)
        except Exception as e:
            print(e)

    def getListOfAtributeFromWebElementList(self, listOfWebElements, attribute):
        newList = []
        if listOfWebElements:
            for elem in listOfWebElements:
                newList.append(elem.get_attribute(attribute))

        return newList

    def getTitleAttributeFromWebElement(self, webElement):
        return webElement.get_attribute('title')

    def getTextFromWebElement(self, webElement):
        return None  # webElement.

    def goBack(self):
        self.driver.back()
