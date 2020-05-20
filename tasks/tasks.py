import luigi
from reddit.praw_connection import RedditPrawConnection
from config import RedditConfig, AppConfig
import pickle
from os import path, makedirs, getcwd, chdir
from middleware.model_generators import submission_model_generator, subreddit_model_generator, CommentModelGenerator
from time import time
import csv


class ScrapeSubreddits(luigi.Task):
    session_id = luigi.Parameter()

    def requires(self):
        return None

    def output(self):
        return luigi.LocalTarget('temp/{session_id}/subreddits.pickle'.format(session_id=self.session_id))

    def run(self):
        reddit = RedditPrawConnection(RedditConfig)
        subreddits = reddit.get_top_subreddits(max_considered_subreddits=3)
        subreddits_list = subreddit_model_generator.get_list(subreddits)

        if not path.exists('temp/{session_id}'.format(session_id=self.session_id)):
            makedirs('temp/{session_id}'.format(session_id=self.session_id))

        with open('temp/{session_id}/subreddits.pickle'.format(session_id=self.session_id), 'wb') as outfile:
            pickle.dump(subreddits_list, outfile)


class ScrapeSubmissions(luigi.Task):
    session_id = luigi.Parameter()

    def requires(self):
        return ScrapeSubreddits(session_id=self.session_id)

    def output(self):
        return luigi.LocalTarget('temp/{session_id}/subreddits'.format(session_id=self.session_id))

    def run(self):
        reddit = RedditPrawConnection(RedditConfig)

        with open('temp/{session_id}/subreddits.pickle'.format(session_id=self.session_id), 'rb') as infile:
            subreddits = pickle.load(infile)

        if not path.exists('temp/{session_id}/subreddits'.format(session_id=self.session_id)):
            makedirs('temp/{session_id}/subreddits'.format(session_id=self.session_id))

        for subreddit in subreddits:
            submissions = reddit.get_submissions_from_subreddit(subreddit, AppConfig.MAX_SUBMISSIONS_PER_SUBREDDIT)
            submission_list = submission_model_generator.get_list(submissions)
            with open('temp/{session_id}/subreddits/{subreddit_name}.pickle'.format(session_id=self.session_id,
                                                                                    subreddit_name=subreddit.display_name),
                      'wb') as outfile:
                pickle.dump(submission_list, outfile)


class CreateDataFrame(luigi.Task):
    session_id = luigi.Parameter()

    def requires(self):
        return ScrapeSubmissions(session_id=self.session_id)

    def output(self):
        return luigi.LocalTarget('scores/scores.csv')

    def run(self):

        reddit = RedditPrawConnection(RedditConfig)

        results = []

        with open('temp/{session_id}/subreddits.pickle'.format(session_id=self.session_id), 'rb') as infile:
            subreddits = pickle.load(infile)

        for subreddit in subreddits:
            info = dict()
            with open('temp/{session_id}/subreddits/{subreddit_display_name}.pickle'.format(session_id = self.session_id,
                                                                                            subreddit_display_name = subreddit.display_name),
                      'rb') as infile:
                submissions = pickle.load(infile)
                for submission in submissions:
                    comments = reddit.get_comments_of_submission(submission)
                    for comment in CommentModelGenerator(comments):
                        submission.add_comment_score(comment.ups)
                    submission.calculate_score()
                    subreddit.add_submission_score(submission.score)
            subreddit.set_num_posts_per_subreddit(AppConfig.MAX_SUBMISSIONS_PER_SUBREDDIT)
            subreddit.calculate_subreddit_score()
            results.append([self.session_id, str(subreddit.display_name), float(subreddit.score)])

        sorted_list = sorted(results, key=lambda x: x[2], reverse=True)

        path_parent = path.dirname(getcwd())
        chdir(path_parent)

        if not path.isfile('scores.csv'):
            with open('scores.csv', 'w', newline='') as newfile:
                writer = csv.writer(newfile)
                writer.writerow(["session_id","subreddit_name","score"])

        with open('scores.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(sorted_list)


if __name__ == '__main__':
    luigi.build([CreateDataFrame(session_id=time())], workers=1, local_scheduler=True)
