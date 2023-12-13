# syntax=docker/dockerfile:1
# This builds an all-in-one easy to install dockerfile

FROM ubuntu:22.04
MAINTAINER Articulon <genixpro@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install gnupg2 gnupg1 gnupg curl -y

# Install some basic system dependencies
RUN apt-get update && apt-get install \
    git \
    python3 \
    python3-pip \
    python3-setuptools \
    unzip \
    vim \
    wget \
     -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/icons/* && \
    rm -f ./path/file -rf /usr/share/man/*

# Create the tussle user
RUN useradd -s /bin/bash --home-dir /home/tussle tussle && \
    mkdir /home/tussle && \
    chown -R tussle:tussle /home/tussle

# Create the folder /tussle to contain the application \
RUN mkdir /tussle

# Copy in the requirements file.
WORKDIR /tussle
COPY requirements.txt .

# Install the dependencies
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install --upgrade cryptography && \
    pip3 install --upgrade grpcio-tools && \
    pip3 install -r requirements.txt && \
    chmod +r+r+r -R /usr/lib/python3/ && \
    rm -rf /root/.cache

# Remove stuff that is no longer needed after the installation
RUN apt purge -y \
         vim \
         gcc \
         build-essential \
         python3-dev && \
    rm -rf /var/log/* && \
    rm -rf /usr/share/icons/* && \
    rm -rf /usr/share/doc/* && \
    rm -rf /usr/share/man/* && \
    rm -rf /var/cache/* && \
    rm -rf /var/lib/dpkg/*
