# All POMs require a webPage object to be instantiated/initialized.
# The webPage object provides the webdriver
import random
from POM import Locators as loc
from POM import MainPage as mpage
from time import sleep


class VA_LogIn:

    def __init__(self, webPage):
        self.page = webPage
        self.driver = self.page.driver

    def logIn(self, user, pswd):

        try:
            self.driver.get("https://thebluesroom.com/login/")
            if self.page.instance.newSession:
                # Remove WebDriver Flag
                success = self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")
                self.driver.get("https://thebluesroom.com/login/")
        except Exception as e:
            print(e)

        if not self.alreadyLoggedIn():
            from random import randint
            sleep(randint(2, 4))
            self.driver.refresh()

            self.page.slowTypeIntoField(loc.loginPage_XPath['userName'], user)
            self.page.slowTypeIntoField(loc.loginPage_XPath['password'], pswd)

            # captcha challenge
            capResponse = self.page.getPageElement_tryHard(loc.loginPage_XPath['captchaTest']).text
            capResponse = self.challenge(capResponse)

            self.page.slowTypeIntoField(loc.loginPage_XPath['captchaResponse'], capResponse)

            self.page.getPageElement_tryHard(loc.loginPage_XPath['LogIn_button']).click()

            sleep(3)

        return mpage.MainPage(self.page)

    def challenge(self, originalString):
        import operator

        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,  # use operator.div for Python 2
            '%': operator.mod,
            '^': operator.xor,
        }

        def eval_binary_expr(op1, oper, op2):
            op1, op2 = int(op1), int(op2)
            return ops[oper](op1, op2)

        order = originalString.split(" e")[0]
        symbols = ['+', '-', '*', '/']

        for symbol in symbols:
            if f'{symbol}' in order:
                a = int(order.split(f' {symbol} ')[0])
                b = int(order.split(f' {symbol} ')[1])

                return ops[symbol](a, b)

    def alreadyLoggedIn(self):
        return False



