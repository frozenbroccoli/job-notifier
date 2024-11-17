from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from .user_agent import user_agent


chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--headless')
chromedriver = webdriver.Chrome(options=chrome_options)
action = ActionChains(chromedriver)
