FROM python:2.7
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt
ADD lifegoals /app
WORKDIR /app
RUN python manage.py collectstatic --no-input
EXPOSE 8000
CMD ["uwsgi", "--ini", "uwsgi.ini"]
