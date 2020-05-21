from config.app_config import AppConfig

def validate_app_config():

    result = True

    app_config = AppConfig()

    max_considered_subreddits = app_config.MAX_CONSIDERED_SUBREDDITS
    max_submissions_per_subreddit = app_config.MAX_SUBMISSIONS_PER_SUBREDDIT
    max_comments_per_submission = app_config.MAX_COMMENTS_PER_SUBMISSION

    result = True if isinstance(max_considered_subreddits, int) else False
    result = True if isinstance(max_submissions_per_subreddit, int) else False
    result = True if isinstance(max_comments_per_submission, int) else False

    result = False if any(
        [max_considered_subreddits, max_submissions_per_subreddit, max_comments_per_submission]) < 0 else True

    if app_config.updated is True:
        print("Updated Configurations from Environment")
    else:
        print("Using default values")

    return result

validate_app_config()