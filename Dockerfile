FROM  ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
ADD . /flask-app
WORKDIR /flask-app
RUN pip install -r requirements.txt
EXPOSE 5566
RUN flask initdb
RUN flask forge
CMD ["flask", "run"]