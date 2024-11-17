import typing


class UrlComponents(typing.NamedTuple):
    scheme: str
    netloc: str
    path: str
    params: str = ''
    query: typing.Optional[str] = ''
    fragment: str = ''


class LinkedInURL:
    """
    LinkedIn URLs used in the project.
    """
    LOGIN = 'https://www.linkedin.com/login/'
    FEED = 'https://www.linkedin.com/feed/'


urls = LinkedInURL()

