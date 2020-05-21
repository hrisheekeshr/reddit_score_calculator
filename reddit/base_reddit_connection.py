import abc

class BaseRedditConnection(abc.ABC):
    """
    Baseclass for reddit adapters. This creates an object with the specified methods to obtain
    informations from reddit APIs
    """

    def connect(self,config):
        """
        Connects to the reddit connection object with configurations.
        :return: Connection Object
        """
        pass

    def get_trending_subreddits(self):
        """
        Given the number of subreddits, it provides a list of trending subreddits.
        :param num_subreddits: int
        :return: list of subreddit objects
        """
        pass


    def get_submissions_from_subreddit(self, subreddit, num_posts:int):
        """
        Given the subreddit id and total number of posts, it returns top submissions from a subreddit
        :param subreddit: subreddit object
        :param num_posts: int
        :return: list of post objects
        """
        pass

    def get_comments_of_submission(self, submission, num_comments:int):
        """
        Gets the comment objects, given a submission ID
        :param submission: submission object
        :param num_comments: int
        :return: comment objecyt
        """
