import os
from utils.logging import Logger

logger = Logger().logger


class RedditConfig:
    """
    Creates the reddit API configurations responsible for scraping data.
    This is essential for getting information from reddit.
    For more information visit : https://github.com/reddit-archive/reddit/wiki/API
    """

    def __init__(self):
        """
        Initialises the global configs for accessing reddit
        """
        self.CLIENT_ID = str()
        self.USER_AGENT = str()
        self.CLIENT_SECRET = str()

        self.set_config_from_environment()

    def set_config_from_environment(self):
        """
        Reads configurations and sets it globally
        :return:
        """
        self.CLIENT_ID = os.environ.get("CLIENT_ID", '*****')
        self.USER_AGENT = os.environ.get("USER_AGENT", '******')
        self.CLIENT_SECRET = os.environ.get("CLIENT_SECRET", '*****')
