import praw
from reddit.base_reddit_connection import BaseRedditConnection
from singleton_decorator import singleton
from utils import Logger

logger = Logger.logger


# noinspection PyBroadException
@singleton
class RedditPrawConnection(BaseRedditConnection):
    """
    Creates the RedditPrawConnection object which is responsible for authenticating reddit APIs to get necessary
    information. It uses the official reddit python sdk : http://praw.readthedocs.io
    """

    def __init__(self, reddit_config):
        self.connection = praw.Reddit(
            client_id = reddit_config.CLIENT_ID,
            client_secret = reddit_config.CLIENT_SECRET,
            user_agent = reddit_config.USER_AGENT
        )
        try:
            logger.debug("Trying to connect to reddit using provided credentials")
            self.connect(reddit_config)
            logger.debug("PRAW Connection Successful")
        except Exception as ex:
            logger.critical("Cannot create PRAW Connection Object due to {}".format(ex))

    def connect(self, reddit_config):
        """
        Authenticates with the reddit API.
        :param reddit_config:
        :return: connection: praw reddit connection object
        """
        return self.connection

    def get_comments_of_submission(self, submission, max_comments_per_submission: int = 5, sort_by="top"):
        """
        :type max_comments_per_submission: int
        :param submission: subreddit comments object
        :param sort_by: str - "confidence", "controversial", "new", "old", "q&a", "top"
        :param max_comments_per_submission: 5
        :return: list of PRAW comment objects from a submission.
        """
        if not type(sort_by) == str:
            raise TypeError("sort_by must be of the type str; provided {}".format(type(sort_by)))

        if sort_by not in ["confidence", "controversial", "new", "old", "q&a", "top"]:
            raise ValueError(
                'Wrong selection. Select one of the options in ["confidence", "controversial", "new", "old", "q&a", '
                '"top"]')

        submission.comment_sort = sort_by
        logger.debug("Comments in this submission are sorted by {}".format(sort_by))
        return list(submission.comments)[0:max_comments_per_submission]

    def get_submissions_from_subreddit(self, subreddit, max_submissions_per_subreddit: int = 10):
        """
        Get a list of submission objects from a subreddit
        :param subreddit: subreddit object
        :param max_submissions_per_subreddit: int - default 10
        :return: list of PRAW submissions objects
        """
        try:
            submissions = list(
                self.connection.subreddit(subreddit.display_name).hot(limit = max_submissions_per_subreddit))
            return submissions
        except Exception as e:
            assert hasattr(subreddit, 'display_name')
            logger.critical("Could not get the submissions due to {}".format(e))

    def get_top_subreddits(self, max_considered_subreddits: int = 50):
        """
        Returns a list of top subreddits
        :param max_considered_subreddits: int
        :return: list of PRAW subreddit objects
        """
        return list(self.connection.subreddits.default(limit = max_considered_subreddits))
