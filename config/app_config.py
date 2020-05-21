import os
from utils.logging import Logger

logger = Logger().logger


class AppConfig:
    """
    Contains the application configurations to be used.
    """

    def __init__(self):
        self.MAX_CONSIDERED_SUBREDDITS = int()
        self.MAX_SUBMISSIONS_PER_SUBREDDIT = int()
        self.MAX_COMMENTS_PER_SUBMISSION = int()

        self.set_config_from_environment()

    def set_config_from_environment(self):
        """
        Sets configuration from environment and sets it globally. Defaults to some values on error
        :return: Nothing
        """
        self.MAX_CONSIDERED_SUBREDDITS = int(os.environ.get('MAX_CONSIDERED_SUBREDDITS', 50))
        self.MAX_SUBMISSIONS_PER_SUBREDDIT = int(os.environ.get('MAX_SUBMISSIONS_PER_SUBREDDIT', 10))
        self.MAX_COMMENTS_PER_SUBMISSION = int(os.environ.get('MAX_COMMENTS_PER_SUBMISSION', 5))
