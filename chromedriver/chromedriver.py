from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

user_agent = UserAgent().random
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chromedriver = webdriver.Chrome(options=chrome_options)
action = ActionChains(chromedriver)
