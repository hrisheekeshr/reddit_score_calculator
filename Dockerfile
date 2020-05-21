FROM spotify/luigi
COPY . .
RUN ["pip", "install", "-r" ,"requirements.txt"]
ENTRYPOINT ["python", "tasks/tasks.py" ]