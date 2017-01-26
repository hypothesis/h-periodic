FROM gliderlabs/alpine:3.4
MAINTAINER Hypothes.is Project and contributors

RUN apk-install \
    python \
    py-pip

# Create the hypothesis user, group, home directory and package directory.
RUN addgroup -S hypothesis && adduser -S -G hypothesis -h /var/lib/h-periodic hypothesis
WORKDIR /var/lib/h-periodic

COPY README.rst requirements.txt start.sh hperiodic.py ./

RUN pip install --no-cache-dir -r requirements.txt

USER hypothesis
CMD ./start.sh
