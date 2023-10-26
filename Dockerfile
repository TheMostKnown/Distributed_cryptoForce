# syntax=docker/dockerfile:1
FROM python:3.10
#FROM ubuntu:latest 
#RUN apt-get install -y python3
#COPY . /engines
COPY /engines .
#WORKDIR  ${projectname}
#WORKDIR ./engines
EXPOSE 6666 9090
#EXPOSE 9090
ENTRYPOINT ["python3"]
CMD ["engine_calc_3_0.py"]
#CMD ["echo", "$PATH"]
