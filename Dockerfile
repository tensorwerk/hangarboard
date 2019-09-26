# Building GUI
FROM node:10.16.3-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY gui/package.json /app/package.json
RUN npm install --silent
RUN npm install react-scripts@3.0.1 -g --silent
COPY gui/* /app/
RUN npm run build

###########################
#  Building Hangar Board  #
###########################

FROM ubuntu:18.04
MAINTAINER hhsecond "sherin@tensorwerk.com"

RUN apt-get update -y && apt-get install -y python3-pip python3-dev

WORKDIR /app
COPY --from=build /app/build /app/static

COPY requirements.txt /app/requirements.txt
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8
RUN pip3 install -r requirements.txt
COPY . /app

ENTRYPOINT /bin/bash entrypoint.sh
