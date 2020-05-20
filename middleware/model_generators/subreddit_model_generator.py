from models import Subreddit


def get_list(subreddits: list):
    return [Subreddit(subreddit) for subreddit in subreddits]


class SubredditModelGenerator:
    """
    Subreddit model generator outputs a generator objects which will yield a subreddit object
    """

    def __init__(self, subreddits: list):
        self.subreddits_generator = (Subreddit(subreddit) for subreddit in subreddits)

    def __iter__(self):
        return self.subreddits_generator
