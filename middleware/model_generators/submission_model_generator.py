from models import Submission


def get_list(submissions: list):
    """
    Returns a list of submission objects
    :param submissions:
    :return: list
    """
    return [Submission(submission) for submission in submissions]


class SubmissionModelGenerator:
    def __init__(self, submissions: list):
        """
        Generates a submission generator object
        :param submissions: list of PRAW submission objects.
        """
        self.submissions_generator = (Submission(submission) for submission in submissions)

    def __iter__(self):
        """
        Can be used as an iterable generator
        ==========================

        Example:

            for submissions in SubmissionModelGenerator():
                do something with submissions

        ==========================
        :return: generator object
        """
        return self.submissions_generator
