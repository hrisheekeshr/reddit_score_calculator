import time
import os

schedule_interval = os.environ.get("SCHEDULE_INTERVAL",12)

def run(session_id):
    os.system("PYTHONPATH=$(pwd) luigi --module tasks.tasks CalculateScores  --local-scheduler --session-id {}".format(session_id))

def sleep_hours(hours):
    time.sleep(hours * 60 * 60)

while True:
    sleep_hours(schedule_interval)
    sleep_hours()