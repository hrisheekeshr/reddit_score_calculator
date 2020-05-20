from models import Comment


class CommentModelGenerator:
    def __init__(self, comments: list):
        self.comments_generator = (Comment(comment) for comment in comments)

    def __iter__(self):
        return self.comments_generator

