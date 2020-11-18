from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'
        self.options = Options()
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('disable-infobars')
        self.options.add_argument('disable-gpu')
        #self.options.add_argument('--headless')
        self.options.add_argument('--incognito')
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36")
        self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=self.options)
        self.login()

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        time.sleep(3)
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()

    def nav_user(self, user):
        self.driver.get('{}/{}/'.format(self.base_url, user))
        self.driver.quit()

if __name__ == '__main__':
    bot = InstagramBot('username', 'password')
    bot.nav_user('username')
