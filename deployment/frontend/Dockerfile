# syntax=docker/dockerfile:1
# This builds an all-in-one easy to install dockerfile

FROM  us-central1-docker.pkg.dev/tussle/tussle-frontend/tussle-frontend-base:latest
MAINTAINER Tussle <genixpro@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ARG TUSSLE_ENV

# Copy the NGINX configuration
ADD deployment/frontend/nginx_config /etc/nginx/sites-enabled/default
RUN sed "s/__TUSSLE_ENV__/${TUSSLE_ENV}/g" -i /etc/nginx/sites-enabled/default

# Copy the source code into the container at /tussle
ADD tussle /tussle/tussle
ADD --chown=tussle:tussle --chmod=777 *.js /tussle
ADD --chown=tussle:tussle --chmod=777 *.json /tussle
ADD --chown=tussle:tussle --chmod=777 .env.* /tussle

# Set the working directory to /tussle, and build the frontend package
WORKDIR /tussle
ENV TUSSLE_ENV=${TUSSLE_ENV}
ENV REVISION_ID=${REVISION_ID}

RUN cp .env.${TUSSLE_ENV} .env.chosen
RUN rm .env.production
RUN mv .env.chosen .env.production

# Build the frontend static files and delete all the tussle code, nodejs and python to trim down the image size
RUN  npm install --force && \
        rm -rf /root/.npm/_cacache && \
        rm -rf /var/cache/* && \
        npm run-script build && \
        mkdir /build && \
        mv build/* /build && \
        rm -rf /tussle && \
        apt-get purge nodejs -y && \
        rm -rf /root/.npm && \
        rm -rf /var/lib/dpkg/* && \
        rm -rf /usr/include/*

RUN mkdir -p /var/log/supervisord
RUN echo "genixpro" > /etc/nginx/fifo
COPY deployment/frontend/supervisord.conf /etc/supervisor/supervisord.conf

# Setup and configure systemd
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf", "-n"]
EXPOSE 80
EXPOSE 443
