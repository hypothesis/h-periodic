FROM alpine:3.7
MAINTAINER Hypothes.is Project and contributors

# Install system and runtime dependencies.
RUN apk add --no-cache libcurl python2 py2-pip

# Create the hypothesis user, group, home directory and package directory.
RUN addgroup -S hypothesis && adduser -S -G hypothesis -h /var/lib/h-periodic hypothesis
WORKDIR /var/lib/h-periodic

COPY README.rst requirements.txt supervisord.conf start.sh hperiodic.py healthcheck.py ./

# Install build deps, build then clean up.
RUN apk add --no-cache --virtual build-deps \
    build-base \
    git \
    curl-dev \
    openssl-dev \
    python-dev \
    && pip install --no-cache-dir -U pip supervisor \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-deps

EXPOSE 8080
USER hypothesis
CMD ./start.sh
