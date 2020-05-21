import unittest
import os

from config import AppConfig


class TestAppConfig(unittest.TestCase):

    def setUp(self) -> None:
        os.environ["MAX_CONSIDERED_SUBREDDITS"] = '3'
        os.environ["MAX_SUBMISSIONS_PER_SUBREDDIT"] = '2'
        os.environ["MAX_COMMENTS_PER_SUBMISSION"] = '2'

        self.app_config = AppConfig()

    def test_max_submissions_per_subreddit_value(self):
        msps = self.app_config.MAX_SUBMISSIONS_PER_SUBREDDIT
        self.assertEqual(msps, 2)


    def test_max_submissions_per_subreddit_type(self):
        msps = self.app_config.MAX_SUBMISSIONS_PER_SUBREDDIT
        self.assertIs(type(msps), int)

    def test_max_considered_subreddits_value(self):
        mcs = self.app_config.MAX_CONSIDERED_SUBREDDITS
        self.assertEqual(mcs, 3)

    def test_max_considered_subreddits_type(self):
        mcs = self.app_config.MAX_CONSIDERED_SUBREDDITS
        self.assertIs(type(mcs) , int)

    def test_max_comments_per_submission_value(self):
        mcps = self.app_config.MAX_COMMENTS_PER_SUBMISSION
        self.assertEqual(mcps, 2)


    def test_max_comments_per_submission_type(self):
        mcps = self.app_config.MAX_COMMENTS_PER_SUBMISSION
        self.assertIs(type(mcps), int)


if __name__ == '__main__':
    unittest.main()
