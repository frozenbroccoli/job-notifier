import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from chromedriver import chromedriver
import interactions
from .credentials import get_credentials
from .urls import urls
from .xpaths import xpaths


def login() -> None:
    """
    Login to LinkedIn.
    :return: None
    """
    chromedriver.implicitly_wait(10)
    if not is_logged_in():
        chromedriver.delete_all_cookies()
        login_url = urls.LOGIN
        chromedriver.get(login_url)
        do_fresh_login()


def is_logged_in() -> bool:
    """
    Check whether the current session is authenticated.
    :return: True if authenticated else False.
    """
    try:
        chromedriver.get(urls.FEED)
        with open('cookies.pkl', 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                chromedriver.add_cookie(cookie)
        try:
            chromedriver.find_element(by=By.XPATH, value=xpaths.SEARCH_BOX)
            return True
        except NoSuchElementException:
            return False
    except FileNotFoundError:
        return False


def do_fresh_login() -> None:
    """
    Do a fresh login into LinkedIn.
    :return:
    """
    username, password = get_credentials().values()
    chromedriver.find_element(by=By.ID, value='username').send_keys(username)
    interactions.make_mouse_movements(1, 3, 1, 3)
    password_box = chromedriver.find_element(by=By.ID, value='password')
    password_box.send_keys(password)
    interactions.wait_randomly(2, 6)
    password_box.send_keys(Keys.RETURN)
    interactions.wait_randomly(3, 4)
    with open('cookies.pkl', 'wb') as file:
        pickle.dump(chromedriver.get_cookies(), file)
