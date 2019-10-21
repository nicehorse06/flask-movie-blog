FROM  ubuntu:18.04
LABEL maintainer="Jimmy Ma <a468963@gmail.com>"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /flask-app
WORKDIR /flask-app
RUN pip3 install -r requirements.txt
EXPOSE 5566
RUN flask initdb
RUN flask forge
CMD ["flask", "run"]