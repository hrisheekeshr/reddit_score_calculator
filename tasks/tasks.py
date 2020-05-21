import luigi
from reddit.praw_connection import RedditPrawConnection
import config
import pickle
from os import path, makedirs, getcwd, chdir
from middleware.model_generators import submission_model_generator, subreddit_model_generator, CommentModelGenerator
from time import time
import csv

app_config = config.AppConfig()
reddit_config = config.RedditConfig()


class ScrapeSubreddits(luigi.Task):
    """
    Get subreddit list from API -----> Convert these objects to app subreddit objects ----> Store in filesystem

    Get subreddit list from API
    ===========================
        Uses the RedditPrawConnection to get the relevant subreddits

    Convert these objects to app subreddit objects
    ==============================================
        Converts the PRAW objects to App objects with methods to calculate subreddit score

    Store in filesystem
    ===================
        These objects are serialised to pickle format and stored in the filesystem.
        https://docs.python.org/3/library/pickle.html

    """
    # Luigi parameter that taken in the unix EPOCH time as session_id
    # This is shared across different tasks to separate data different runs
    session_id = luigi.Parameter()

    def requires(self):
        return None

    def output(self):
        # Scraped data is stored in a folder called "data/{unix epoch time}/subreddits.pickle"
        return luigi.LocalTarget('data/{session_id}/subreddits.pickle'.format(session_id = self.session_id))

    def run(self):
        # Creates the reddit object
        reddit = RedditPrawConnection(reddit_config)

        # Gets the list of PRAW subreddit objects
        subreddits = reddit.get_top_subreddits(max_considered_subreddits = app_config.MAX_CONSIDERED_SUBREDDITS)

        # Converts the list of subreddits to the app object models
        subreddits_list = subreddit_model_generator.get_list(subreddits)

        # Creates new folder under the data directory
        if not path.exists('data/{session_id}'.format(session_id = self.session_id)):
            makedirs('data/{session_id}'.format(session_id = self.session_id))

        # Creates a pickle file and writes out the binary data to the filesystem.
        with open('data/{session_id}/subreddits.pickle'.format(session_id = self.session_id), 'wb') as outfile:
            pickle.dump(subreddits_list, outfile)


class ScrapeSubmissions(luigi.Task):
    """
    Get subreddit list from filesystem -----> Get all submissions for each subreddit --->
    -----> Store each subreddit in a directory in filesystem

    Get subreddit list from filesystem
    ===========================
        Load the pickle file to get subreddit objects

    Get all submissions for each subreddit
    ==============================================
        Iterate through all subreddits to get submissions for each subreddit

    Store in filesystem
    ===================
        Files are named by their subreddit display names and stored in the file system.
    """
    # Luigi parameter that taken in the unix EPOCH time as session_id
    # This is shared across different tasks to separate data different runs
    session_id = luigi.Parameter()

    def requires(self):
        return ScrapeSubreddits(session_id = self.session_id)

    def output(self):
        return luigi.LocalTarget('data/{session_id}/subreddits'.format(session_id = self.session_id))

    def run(self):
        # Creates a reddit API connection
        reddit = RedditPrawConnection(reddit_config)

        # Deserializes the subreddit objects from file
        with open('data/{session_id}/subreddits.pickle'.format(session_id = self.session_id), 'rb') as infile:
            subreddits = pickle.load(infile)

        # Creates a directory to store subreddit submissions
        if not path.exists('data/{session_id}/subreddits'.format(session_id = self.session_id)):
            makedirs('data/{session_id}/subreddits'.format(session_id = self.session_id))

        # Iterates through each subreddits
        for subreddit in subreddits:
            # Gets submissions from subreddits
            submissions = reddit.get_submissions_from_subreddit(subreddit, app_config.MAX_SUBMISSIONS_PER_SUBREDDIT)

            # Convert the PRAW objects to app objects
            submission_list = submission_model_generator.get_list(submissions)

            # Store each subreddit submissions in different pickle files. 
            with open('data/{session_id}/subreddits/{subreddit_name}.pickle'.format
                          (session_id = self.session_id, subreddit_name = subreddit.display_name), 'wb') as outfile:
                pickle.dump(submission_list, outfile)


class CalculateScores(luigi.Task):
    """
    This task Deserialize Subreddits from the file system and iterates thorugh it.
    During each run, it loads up the corresponding submissions for that subreddit and loads the comment object
    Iterates through each comment object to add the comment scores to the submission.
    Finally, It calculates the subreddit scores and dumps it into a CSV
    """
    # Luigi parameter that taken in the unix EPOCH time as session_id
    # This is shared across different tasks to separate data different runs
    session_id = luigi.Parameter()

    def requires(self):
        return ScrapeSubmissions(session_id = self.session_id)

    def output(self):
        return luigi.LocalTarget('data/scoress.csv')

    def run(self):

        # Creates a reddit connection
        reddit = RedditPrawConnection(reddit_config)

        # Initialised a list to store final results of this run.
        # This list will be written to the csv at the end of the run
        results = []

        # Deserializes the pickle file stored under a session
        with open('data/{session_id}/subreddits.pickle'.format(session_id = self.session_id), 'rb') as infile:
            subreddits = pickle.load(infile)

        # For each subreddit object in the subreddit object list
        for subreddit in subreddits:
            # Opens and loads corresponding submissions from the filesystem
            with open(
                    'data/{session_id}/subreddits/{subreddit_display_name}.pickle'.format
                        (session_id = self.session_id, subreddit_display_name = subreddit.display_name),
                    'rb') as infile:
                submissions = pickle.load(infile)

                # For each submission object in submission object list
                for submission in submissions:

                    # Loads the comments from submission
                    comments = reddit.get_comments_of_submission(submission, max_comments_per_submission = app_config.MAX_COMMENTS_PER_SUBMISSION)

                    # For each comment object in list of comment objects
                    for comment in CommentModelGenerator(comments):
                        # Adds comment upvote scores to the submission
                        submission.add_comment_score(comment.ups)

                    # Calculates the score of that submission
                    submission.calculate_score()

                    # Adds the submission score to the subreddit
                    subreddit.add_submission_score(submission.score)

            # Sets the maximum number of posts from the app config
            subreddit.set_num_posts_per_subreddit(app_config.MAX_SUBMISSIONS_PER_SUBREDDIT)

            # Calculates the subreddit scores
            subreddit.calculate_subreddit_score()

            # Appends the subreddit scores to the results list
            results.append([self.session_id, str(subreddit.display_name), float(subreddit.score)])

        # Sorts the final list of objects
        sorted_list = sorted(results, key = lambda x: x[2], reverse = True)

        # Goes up in one directory
        # path_parent = path.dirname(getcwd())
        # chdir(path_parent)

        # Creates a new file named scores.csv
        if not path.isfile('data/scores.csv'.format(session_id = self.session_id)):
            with open('data/scores.csv'.format(session_id=self.session_id), 'w', newline = '') as newfile:
                writer = csv.writer(newfile)
                writer.writerow(["session_id", "subreddit_name", "score"])

        # Appends the new scores list to the CSV
        with open('data/scores.csv'.format(session_id=self.session_id), 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerows(sorted_list)

if __name__ == '__main__':
    luigi.build([CalculateScores(session_id = time())], workers = 1, local_scheduler = True)
