# Reddit Score Calculator

![Build](https://github.com/hrisheekeshr/reddit_score_calculator/workflows/Python%20application/badge.svg)
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/rhrisheekesh/luigi-reddit)

This repository contains a code that does the following things

  - Scrapes top subreddits from reddit (configurable)
  - Calculates the score of these subreddits
  - The result CSV has the following columns: 
    - session_id : unix epoch time or any float
    - subreddit name : name of the subreddit
    - score : subreddit score

# Get Started with Docker Images

## Run the container

```sh
docker run \\
-v $(pwd):/data \\
--env CLIENT_ID={client_id} \\
--env USER_AGENT={user-agent} \\
--env CLIENT_SECRET={client-secret} \\
rhrisheekesh/luigi-reddit:latest
```

## View Results

If you mount the /data directory, it has subfolders denoting each run. The subfolder name is according to the linux epoch time of run. 

It also has a csv, scores.csv which has the aggregate results of all runs

In the future, this can later be replaced with a database if required.



## Building the image manually

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

# Developing without Docker

## Code

Code is well documented with docstrings including examples, return types and params. Please refer to the code for more details

## Testing 

I have used python unittest for testing. 


Go to the root directory and run :
```sh
bash tests.sh 
```
alternatively you can do

```python
 python -m unittest discover -s tests
```

## Running

To run the code, 
```python
 python run.py
```

# CI

This repository is integrated to an automatic build systems - Github Actions. The YML files are in the root of this repository under .github directory.

