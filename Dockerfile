# this is a comment file for Docker
FROM ubuntu:14.04
RUN apt-get update
RUN apt-get -y install git python python-dev python-pip
RUN pip install flask Flask-Bootstrap Flask-SQLAlchemy Flask-Mail
RUN git clone https://github.com/dodoru/flask_todo
EXPOSE 5000
CMD ["/usr/bin/python","/flask_todo/app.py"]
