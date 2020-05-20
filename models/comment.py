class Comment:

    def __init__(self, comment):
        self.id = comment.name
        self.ups = comment.ups
        self.submission_id = comment.parent_id

    def __repr__(self):
        return "<Comment(name='%s',parent_submission='%s', upvotes='%d')>" % (
            self.id, self.submission_id, self.ups)