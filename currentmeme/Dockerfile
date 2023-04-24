FROM python:latest

ADD ./ docker_compose/python
WORKDIR docker_compose/python
ENV PATH=$PATH:/docker_compose/python
ENV PYTHONPATH /docker_compose/python
RUN pip install PyMySQL
RUN pip install cryptography
RUN pip install jarowinkler
RUN pip install -U discord.py[voice]
RUN pip install requests
RUN pip install ffmpeg-python
RUN pip install deepgram-sdk
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg