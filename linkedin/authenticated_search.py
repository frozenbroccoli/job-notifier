import time
import re
import typing
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from chromedriver.chromedriver import chromedriver
import interactions
from .xpaths import xpaths


def search_jobs(
        query: str,
        date_posted: str = '',
        experience_level: typing.Tuple = (None,),
        company: typing.Tuple = (None,),
        mode: typing.Tuple = (None,),
        easy_apply: bool = False
) -> typing.List:
    """
    Search for jobs on LinkedIn assuming the post-login
    landing page is open.
    :return: List of jobs.
    """
    initiate_search(query)
    interactions.wait_randomly(2, 5)
    interactions.make_mouse_movements(1, 3, 1, 3)
    try:
        customize(
            date_posted,
            experience_level,
            company,
            mode,
            easy_apply
        )
        interactions.wait_randomly(2, 4)
    except NoSuchElementException:
        print('Not found')

    return []


def customize(
        date_posted: str = '',
        experience_level: typing.Tuple = (None,),
        company: typing.Tuple = (None,),
        mode: typing.Tuple = (None,),
        easy_apply: bool = False
) -> None:
    """
    Customize the search by selecting the filters.
    :param date_posted: Date posted filter.
    :param experience_level: Experience level filter.
    :param company: Company filter.
    :param mode: Mode filter (Remote, In office, Hybrid)
    :param easy_apply: If easy apply is available.
    :return: None
    """
    num_results = 0

    def if_num_results_available(*args) -> bool:
        """
        Check if the number of search results is available
        in the button.
        :param args: Webdriver.
        :return: True if num_results available else False
        """
        nonlocal num_results
        return (num_results := get_num_results(show_results_button)) is not None

    chromedriver.find_element(by=By.XPATH, value=xpaths.DATE_POSTED_BUTTON).click()
    interactions.scroll_randomly(2)
    if date_posted:
        match date_posted:
            case 'any_time':
                option = chromedriver.find_element(by=By.XPATH, value=xpaths.ANY_TIME_OPTION)
            case 'past_month':
                option = chromedriver.find_element(by=By.XPATH, value=xpaths.PAST_MONTH_OPTION)
            case 'past_week':
                option = chromedriver.find_element(by=By.XPATH, value=xpaths.PAST_WEEK_OPTION)
            case 'past_day':
                option = chromedriver.find_element(by=By.XPATH, value=xpaths.PAST_DAY_OPTION)
            case _:
                raise ValueError('Unacceptable argument for date_posted')
        option.click()
        interactions.make_mouse_movements(1, 2, 2, 5)
        show_results_button = chromedriver.find_element(by=By.XPATH, value=xpaths.SHOW_RESULTS_BUTTON)
        wait = WebDriverWait(chromedriver, 5)
        wait.until(if_num_results_available)
        print(f'{num_results=}')
        show_results_button.click()


def get_num_results(button: WebElement) -> typing.Union[int, None]:
    """
    Get the number of search results from the "Show Results"
    button.
    :return: Number of search results.
    """
    try:
        text = button.get_attribute('aria-label')
        print(f'-------------{text=}---------------')
        return int(re.search(r'\d+', text).group())
    except AttributeError:
        return None


def initiate_search(query: str) -> None:
    """
    Initiate the search. Puts the query in the search box
    and hits Enter.
    :param query: Keywords to search for.
    :return: None
    """
    search_box = chromedriver.find_element(by=By.XPATH, value=xpaths.SEARCH_BOX)
    search_box.send_keys(query)
    interactions.wait_randomly(2, 5)
    search_box.send_keys(Keys.RETURN)
    try:
        interactions.scroll_randomly(5)
        chromedriver.find_element(by=By.XPATH, value=xpaths.JOBS_BUTTON).click()
    except NoSuchElementException:
        chromedriver.find_element(by=By.XPATH, value=xpaths.POSTS_BUTTON).click()
        chromedriver.find_element(by=By.XPATH, value=xpaths.DROPDOWN_JOBS_OPTION).click()
