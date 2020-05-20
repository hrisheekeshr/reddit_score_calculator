class Submission:
    def __init__(self, submission):
        self.__total_comment_score = float(0)
        self.id = submission.name
        self.subreddit_id = submission.subreddit_id
        self.num_comments = submission.num_comments
        self.ups = submission.ups
        self.score = float(0)
        self.comments = submission.comments

    def add_comment_score(self, comment_score: float):
        self.__total_comment_score += comment_score

    def calculate_score(self):
        try:
            self.score = self.__total_comment_score / float(self.num_comments)
        except ZeroDivisionError:
            self.score = float(0)

    def __repr__(self):
        return "<Submission(id='%s',score='%d', total_comment_score='%d')>" % (
            self.id, self.score, self.__total_comment_score)
