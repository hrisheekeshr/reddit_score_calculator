from models import Comment


class CommentModelGenerator:
    """
    Returns a list of subreddit objects
    :param comments: list of PRAW comment objects
    :return: generator object
    """
    def __init__(self, comments: list):
        self.comments_generator = (Comment(comment) for comment in comments)

    def __iter__(self):
        """
        Can be used as an iterable
        ==========================

        Example:

            for comments in CommentModelGenerator():
                do something with comments

        ==========================
        :return: generator object
        """
        return self.comments_generator

