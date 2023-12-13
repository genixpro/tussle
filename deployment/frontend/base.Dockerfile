# syntax=docker/dockerfile:1
# This builds an all-in-one easy to install dockerfile

FROM       debian:bookworm
MAINTAINER Articulon <genixpro@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install curl gnupg ca-certificates -y
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
ENV NODE_MAJOR=20
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list

# Install some basic system dependencies
RUN apt-get update && apt-get install \
      nginx \
      supervisor \
      nodejs  \
      -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/icons/* && \
    rm -f ./path/file -rf /usr/share/man/*


# We add package.json here in the base image, so that
# the base image can preinstall most of the dependencies
RUN mkdir /tussle

# Set the working directory to /tussle
WORKDIR /tussle
COPY package.json /tussle
COPY package-lock.json /tussle
WORKDIR /tussle
RUN npm install --force && \
    rm -rf /root/.npm/_cacache && \
    rm -rf /var/cache/*
