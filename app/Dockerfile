FROM python:latest

ADD ./app/code/requirements.txt /code/requirements.txt

WORKDIR /code

RUN pip3 install -r requirements.txt

# CMD ["python3", "main.py"]
# CMD ["uwsgi", "--http", ":80", "--wsgi-file", "main.py", "--callable", "app", "--processes", "4", "--threads", "2", "--py-autoreload", "1", "--stats", ""]
CMD ["uwsgi", "--ini", "uwsgi.ini"]
