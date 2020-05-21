from models import Subreddit


def get_list(subreddits: list):
    """
    Returns a list of subreddit objects
    :param subreddits:
    :return: list
    """
    return [Subreddit(subreddit) for subreddit in subreddits]


class SubredditModelGenerator:
    """
    Subreddit model generator outputs a generator objects which will yield a subreddit object
    """

    def __init__(self, subreddits: list):
        self.subreddits_generator = (Subreddit(subreddit) for subreddit in subreddits)

    def __iter__(self):

        """
        Can be used as an iterable generator
        ==========================

        Example:

            for subreddit in SubredditModelGenerator():
                do something with subreddits

        ==========================
        :return: generator object
        """
        return self.subreddits_generator
