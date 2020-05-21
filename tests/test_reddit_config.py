import unittest
import os

from config import RedditConfig


class TestAppConfig(unittest.TestCase):

    def setUp(self) -> None:
        os.environ["CLIENT_ID"] = 'client_id'
        os.environ["USER_AGENT"] = 'user_agent'
        os.environ["CLIENT_SECRET"] = 'client_secret'

        self.reddit_config = RedditConfig()

    def test_client_id(self):
        cid = self.reddit_config.CLIENT_ID
        self.assertEqual(cid, 'client_id')
        self.assertIs(type(cid), str)

    def test_user_agents(self):
        ua = self.reddit_config.USER_AGENT
        self.assertEqual(ua, 'user_agent')
        self.assertIs(type(ua), str)

    def test_client_secret(self):
        cs = self.reddit_config.CLIENT_SECRET
        self.assertEqual(cs, 'client_secret')
        self.assertIs(type(cs), str)


if __name__ == '__main__':
    unittest.main()
