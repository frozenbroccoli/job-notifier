"""
LinkedIn's credentials.
"""
import os
import typing
from dotenv import load_dotenv


load_dotenv()


def get_credentials() -> typing.Dict:
    """
    Get LinkedIn's credentials for login.
    :return: Dictionary with credentials.
    """
    return {
        'email': os.getenv('LINKEDIN_USERNAME'),
        'password': os.getenv('LINKEDIN_PASSWORD')
    }
