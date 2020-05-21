class Subreddit:
    """
    This is the base data model for a subreddit
    """

    def __init__(self, subreddit):
        self.__total_submission_score = float(0)
        self.__num_posts_per_subreddit = float(0)
        self.display_name = subreddit.display_name
        self.id = subreddit.name
        self.subreddit_name_prefixed = subreddit.display_name_prefixed
        self.subscribers = subreddit.subscribers
        self.score = float(0)

    def set_num_posts_per_subreddit(self, value):
        """
        Sets the number of posts per subreddit. Default set to the read from app config
        :param value:
        :return: None
        """
        self.__num_posts_per_subreddit = value

    def get_num_posts_per_subreddit(self):
        """
        Gets the current value of number of posts per subreddit
        :return: int
        """
        return self.__num_posts_per_subreddit

    def add_submission_score(self, score):
        self.__total_submission_score += score

    def calculate_subreddit_score(self):
        """
        Calculates the subreddit score
        :return:
        """
        try:
            self.score = self.__total_submission_score / self.__num_posts_per_subreddit
        except ZeroDivisionError:
            self.score = float(0)

    def __repr__(self):
        return "<Subreddit(name='%s',subscribers='%d', score='%d')>" % (
            self.subreddit_name_prefixed, self.subscribers, self.score)
