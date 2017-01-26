FROM gliderlabs/alpine:3.4
MAINTAINER Hypothes.is Project and contributors

RUN apk-install \
    python \
    py-pip \
    && pip install --no-cache-dir -U pip supervisor

# Create the hypothesis user, group, home directory and package directory.
RUN addgroup -S hypothesis && adduser -S -G hypothesis -h /var/lib/h-periodic hypothesis
WORKDIR /var/lib/h-periodic

COPY README.rst requirements.txt supervisord.conf start.sh hperiodic.py ./

RUN pip install --no-cache-dir -r requirements.txt

USER hypothesis
CMD ./start.sh
