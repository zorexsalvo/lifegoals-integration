FROM python:2.7
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt
ADD lifegoals /app
WORKDIR /app
EXPOSE 8000
CMD ["uwsgi", "--ini", "uwsgi.ini"]
