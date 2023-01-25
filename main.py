import Bot

# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
#
# driver = webdriver.Chrome(ChromeDriverManager().install())

bot = Bot.InstaBot()
bot.logIn()
bot.getAvideo()