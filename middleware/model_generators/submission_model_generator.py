from models import Submission


def get_list(submissions: list):
    return [Submission(submission) for submission in submissions]


class SubmissionModelGenerator:
    def __init__(self, submissions: list):
        self.submissions_generator = (Submission(submission) for submission in submissions)

    def __iter__(self):
        return self.submissions_generator
