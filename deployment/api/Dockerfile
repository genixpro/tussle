# syntax=docker/dockerfile:1
# This builds an all-in-one easy to install dockerfile

FROM  us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api-base:latest
MAINTAINER Articulon <genixpro@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

# Set the working directory to /tussle
WORKDIR /tussle

# Copy the current directory contents into the container at /tussle
ADD tussle/ /tussle/tussle
ADD requirements.txt /tussle
ADD setup.py /tussle
ADD README.md /tussle

# Install dependencies for server
WORKDIR /tussle
RUN python3 setup.py install && \
    rm -rf /root/.cache && \
    chmod +r+r+r -R /usr/lib/python3/

ARG ARTICULON_ENV
ARG REVISION_ID
ENV ARTICULON_ENV=${ARTICULON_ENV}
ENV REVISION_ID=${REVISION_ID}


ENV HOME=/home/tussle
RUN chown -R tussle:tussle /tussle && \
    chown -R tussle:tussle /home/tussle && \
    chmod ugo+r -R /usr/lib/python3

RUN rm -rf /usr/include/*

WORKDIR /home/tussle
RUN chmod ugo+r -R /usr/lib/python3 && chown -R tussle:tussle /home/tussle
WORKDIR /tussle

# Output all the disk usage for various folders on the system.
# This helps us to further optimize the container
# RUN du -h -d 5 -t 10M /; exit 0

USER tussle:tussle

# Run the rapid internal test suite. This isn't a full test suite but will catch some
# errors in the configuration or installation.
#RUN tussle_run_rapid_internal_test_suite

# Setup and configure systemd
ENTRYPOINT ["bash", "-c", "tussle_server"]

EXPOSE 5496
