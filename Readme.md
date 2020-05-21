# Reddit Score Calculator

![Build](https://github.com/hrisheekeshr/reddit_score_calculator/workflows/Python%20application/badge.svg)

This repository contains a code that does the following things

  - Scrapes top subreddits from reddit (configurable)
  - Calculates the score of these subreddits
  - The result CSV has the following columns: 
    - session_id : unix epoch time or any float
    - subreddit name : name of the subreddit
    - score : subreddit score

# Get Started
## Run the container

```sh
docker run \\
-v data:app/data \\
--env CLIENT_ID={client_id} \\
--env USER_AGENT={user-agent} \\
--env CLIENT_SECRET={client-secret} \\
rhrisheekesh/luigi-reddit:latest
```
## View Results
The results can be viewed at 'scores.csv' situated at the root directory
# Testing

Go to the root directory and run :
```sh
bash tests.sh 
```
alternatively you can

```python
 python -m unittest discover -s tests
```

# Building

This whole pipeline is dockerised. To build the docker image
```sh
docker build \\
--build-arg CLIENT_ID={client id} \\
--build-arg USER_AGENT={user-agent} \\
--build-arg CLIENT_SECRET={client-secret} \\
--build-arg MAX_SUBMISSIONS_PER_SUBREDDIT=2 \\
--build-arg MAX_COMMENTS_PER_SUBMISSION=2  \\
--build-arg MAX_CONSIDERED_SUBREDDITS=2 \\
--build-arg SCHEDULE_INTERVAL=12 -t luigi-reddit .
```
All of these variables can be overridden during run. The env variable names are self explanatory. 

For easiness of use, this repository is configured for automated builds in [Dockerhub](https://hub.docker.com/repository/docker/rhrisheekesh/luigi-reddit)

