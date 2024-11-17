import typing
import re
import requests
from urllib.parse import urlunparse, urlencode
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from .urls import UrlComponents


def map_job_arrangements(job_arrangements: typing.List[typing.Literal['onSite', 'hybrid', 'remote']]):
    arrangement_map = {
        'onSite': '1',
        'hybrid': '2',
        'remote': '3'
    }
    return [arrangement_map[arrangement] for arrangement in job_arrangements if arrangement in arrangement_map]


def construct_search_url(
        keywords: str,
        location: str,
        distance: int,
        job_type: str,
        time_posted: str,
        job_arrangements: typing.List[typing.Literal['onSite', 'hybrid', 'remote']],
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
    :param job_arrangements: On-site, remote, etc.
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

    f_wt = ','.join(map_job_arrangements(job_arrangements))

    query_params = urlencode(
        {
            'keywords': keywords,
            'location': location,
            'distance': distance,
            'f_JT': f_jt,
            'f_TPR': f_tpr,
            'f_WT': f_wt,
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
        job_arrangements: typing.List[typing.Literal['onSite', 'hybrid', 'remote']],
        num_results: int
) -> typing.List[typing.Dict]:
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
    :param job_arrangements: The preferred arrangement of the job.
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
            job_arrangements=job_arrangements,
            start=it * 10 + 1
        )
        print(f'Search URL: {search_url}')
        for _ in range(15):
            user_agent = UserAgent().random
            response = requests.get(url=str(search_url), headers={'content-type': 'html', 'User-Agent': user_agent})
            soup = BeautifulSoup(response.text, features='html.parser')
            listings = soup.find_all('div', class_=re.compile(r'base-card relative'))
            if listings:
                job_listings += listings
                break
    response = []
    for job in job_listings:
        try:
            job_title = job.find('h3', class_='base-search-card__title').get_text(strip=True)
            job_url = job.find('a', class_=re.compile(r'base-card__full-link'))['href']
            company_name = job.find('h4', class_='base-search-card__subtitle').get_text(strip=True)
            location = job.find('span', class_='job-search-card__location').get_text(strip=True)
            hiring_status = job.find('span', class_='job-posting-benefits__text').get_text(strip=True)
            posting_time = job.find('time', class_='job-search-card__listdate--new').get_text(strip=True)

            response.append(
                {
                    'job_title': job_title,
                    'job_url': job_url,
                    'company_name': company_name,
                    'location': location,
                    'hiring_status': hiring_status,
                    'posting_time': posting_time
                }
            )
        except AttributeError:
            pass

    return response
