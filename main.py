import typing
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


def get_if_contains(elem: Tag, keyword: str) -> typing.Union[str, None]:
    """
    Return the text of a bs4 tag if it contains a keyword.
    :param elem: The bs4 tag.
    :param keyword: The keyword being looked for.
    :return: Text content of the tag or None.
    """
    if keyword in (text := elem.text):
        return text
    return None


def main() -> None:
    """
    Main function.
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


if __name__ == '__main__':
    main()
