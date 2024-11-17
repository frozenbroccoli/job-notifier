import time
import re
import typing
from urllib.parse import urlunparse, urlencode
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from chromedriver import chromedriver, user_agent
import interactions
from .xpaths import xpaths


class UrlComponents(typing.NamedTuple):
    scheme: str
    netloc: str
    path: str
    params: str = ''
    query: typing.Optional[str] = ''
    fragment: str = ''


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


def construct_search_url(
        keywords: str,
        location: str,
        distance: int,
        job_type: str,
        time_posted: str,
        job_arrangement: str,
        start: int
) -> str:
    """
    Create a URL from the query params for an unauthenticated
    LinkedIn search.
    :param keywords: Search keywords.
    :param location: Desired job location.
    :param distance: Max distance of job from desired location in kms.
    :param job_type: Type of job, full-time, part-time, etc.
    :param time_posted: Job posting time relative to time of search.
    :param job_arrangement: On-site, remote, etc.
    :param start: Start index of search results.
    :return: The search url.
    """
    match job_type:
        case 'fullTime':
            f_jt = 'F'
        case 'partTime':
            f_jt = 'P'
        case 'contractual':
            f_jt = 'C'
        case 'internships':
            f_jt = 'I'
        case 'volunteer':
            f_jt = 'V'
        case _:
            raise ValueError(
                f'Job type {job_type} is not fullTime, partTime, contractual internships or volunteer'
            )

    match time_posted:
        case 'pastDay':
            f_tpr = 'r86400'
        case 'pastWeek':
            f_tpr = 'r604800'
        case 'pastMonth':
            f_tpr = 'r2592000'
        case _:
            raise ValueError(f'Time posted {time_posted} is not pastDay, pastWeek, or pastMonth')

    arrangements = []
    if 'onSite' in job_arrangement:
        arrangements.append('1')
    if 'hybrid' in job_arrangement:
        arrangements.append('2')
    if 'remote' in job_arrangement:
        arrangements.append('3')
    f_jt = ','.join(arrangements)

    query_params = urlencode(
        {
            'keywords': keywords,
            'location': location,
            'distance': distance,
            'f_JT': f_jt,
            'f_TPR': f_tpr,
            'f_WT': f_jt,
            'start': start
        }
    )
    return str(
        urlunparse(
            UrlComponents(
                scheme='https',
                netloc='in.linkedin.com',
                path='/jobs-guest/jobs/api/seeMoreJobPostings/search',
                query=query_params
            )
        )
    )


def get_job_listings(
        keywords: str,
        location: str,
        distance: int,
        job_type: str,
        time_posted: str,
        job_arrangement: str,
        num_results: int
) -> typing.List:
    """
    Search the LinkedIn job board without authentication.
    :param keywords: The search keywords for the job.
    :param location: The location of the job.
    :param distance: The radius of the job from the given location
        in kilometers.
    :param job_type: The type of the job. Options are fullTime,
        partTime, contractual, internships, and volunteer.
    :param time_posted: Time of posting of the job relative to the
        time of search. The options are 'pastDay', 'pastWeek', and
        'pastMonth'.
    :param job_arrangement: The preferred arrangement of the job.
        The options are 'onSite', 'hybrid', and 'remote'.
    :param num_results: The number of search results required.
    :return: The search results.
    """
    job_listings = []
    for it in range(num_results // 10):
        search_url = construct_search_url(
            keywords=keywords,
            location=location,
            distance=distance,
            job_type=job_type,
            time_posted=time_posted,
            job_arrangement=job_arrangement,
            start=it * 10 + 1
        )
        for _ in range(10):
            response = requests.get(url=str(search_url), headers={'content-type': 'html', 'User-Agent': user_agent})
            soup = BeautifulSoup(response.text, features='html.parser')
            listings = soup.find_all('div', class_='base-search-card__info')
            if listings:
                job_listings += listings
                break
    response = []
    for job in job_listings:
        job_title = job.find('h3', class_='base-search-card__title').get_text(strip=True)
        company_name = job.find('h4', class_='base-search-card__subtitle').get_text(strip=True)
        location = job.find('span', class_='job-search-card__location').get_text(strip=True)
        hiring_status = job.find('span', class_='job-posting-benefits__text').get_text(strip=True)
        posting_time = job.find('time', class_='job-search-card__listdate--new').get_text(strip=True)

        response.append(
            {
                'job_title': job_title,
                'company_name': company_name,
                'location': location,
                'hiring_status': hiring_status,
                'posting_time': posting_time
            }
        )

    return response
