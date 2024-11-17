import typing
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import linkedin


def get_if_contains(elem: Tag, keyword: str) -> typing.Union[str, None]:
    """
    Return the text of a bs4 tag if it contains a keyword.
    :param elem: The bs4 tag.
    :param keyword: The keyword being looked for.
    :return: Text content of the tag or None.
    """
    return text if keyword in (text := elem.get_text()) else None


def give_demo() -> None:
    """
    Beautiful soup demo.
    :return: None
    """
    page = requests.get(
        url='https://beautiful-soup-4.readthedocs.io/en/latest/#making-the-soup',
        headers={'content-type': 'html'}
    ).text
    soup = BeautifulSoup(page, features='html.parser')
    paragraphs = [
        valid for elem in soup.find_all('p') if (valid := get_if_contains(elem, 'soup')) is not None
    ]
    print(paragraphs)


def main() -> None:
    """
    Main function.
    :return: None
    """
    # linkedin.login()
    # interactions.wait_randomly(3, 6)
    # linkedin.search_jobs(
    #     query='react js',
    #     date_posted='past_day'
    # )
    results = linkedin.get_job_listings(
        keywords='React+Developer',
        location='Hyderabad',
        distance=25,
        job_type='fullTime',
        time_posted='pastDay',
        job_arrangement='onSite',
        num_results=30
    )
    print(results)
    # response = requests.get(
    #     url=url,
    #     headers={'content-type': 'html'}
    # )
    # # with open('results.html', 'w') as file:
    # #     file.write(response.text)
    #
    # print(response.text)
    # pass


if __name__ == '__main__':
    main()
