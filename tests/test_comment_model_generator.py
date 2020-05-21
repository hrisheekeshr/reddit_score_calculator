import unittest
from models import Comment
from middleware.model_generators import CommentModelGenerator

class MockCommentObject:

    def __init__(self , name , ups , parent_id):
        self.name = str
        self.ups = int
        self.parent_id = str


mock_comment_1 = MockCommentObject(name = "a" , ups = 12 , parent_id = "parent_a")
mock_comment_2 = MockCommentObject(name = "b" , ups = 12 , parent_id = "parent_b")
mock_comment_list = [mock_comment_1, mock_comment_2]


class TestCommentModelGenerator(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_comment_list = mock_comment_list


    def test_comment_object_type(self):
        comments = CommentModelGenerator(mock_comment_list)

        for comment in comments:
            self.assertIsInstance(comment,Comment)


if __name__ == '__main__':
    unittest.main()
