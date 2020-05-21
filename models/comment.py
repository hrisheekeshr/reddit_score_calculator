class Comment:
    """
    So, this is the base model for comments that we use in the app. This is being built from an object with the params.
    """

    def __init__(self, comment):
        """
        Constructor object. Make sure the the comment object has those params
        :param comment: comment object with params name, ups and parent_id ( the submission id )
        """
        self.id = comment.name
        self.ups = comment.ups
        self.submission_id = comment.parent_id

    def __repr__(self):
        return "<Comment(name='%s',parent_submission='%s', upvotes='%d')>" % (
            self.id, self.submission_id, self.ups)