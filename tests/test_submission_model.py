import unittest
from models import Comment, Submission


class MockSubmissionObject:

    def __init__(self , name , sub_name , num_comments , ups, comments ):
        self.name: str = name
        self.subreddit_id: str = sub_name
        self.num_comments: int = num_comments
        self.ups: int = ups
        self.comments = None

class TestSubmissionModel(unittest.TestCase):

    def setUp(self) -> None:
        # Create a submission model
        self.mock_submission = MockSubmissionObject(
                        name = 'mock_submission',
                        sub_name = "mock_subreddit",
                        num_comments = 10,
                        ups = 3,
                        comments = None
                        )

        self.submission_model = Submission(self.mock_submission)

    def test_add_comment_score(self):
        self.submission_model.add_comment_score(5)
        self.assertEqual(self.submission_model.get_comment_score(), 5)
        self.submission_model.add_comment_score(-5)

    def test_num_comments_zero(self):
        self.submission_model.num_comments = 0
        self.submission_model.calculate_score()
        self.assertEqual(self.submission_model.score, 0)

    def test_calculate_score(self):
        self.submission_model.num_comments = 10
        self.submission_model.add_comment_score(4)
        self.submission_model.add_comment_score(3)
        self.submission_model.add_comment_score(2)
        self.submission_model.calculate_score()

        # sum = 4 + 3 + 2 = 9
        # score = 9 / 10 = 0.9
        self.assertEqual(self.submission_model.score,0.9)

if __name__ == '__main__':
    unittest.main()
