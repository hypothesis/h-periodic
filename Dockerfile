FROM python:3.8.12-alpine3.13
MAINTAINER Hypothes.is Project and contributors

# Create the h-periodic user, group, home directory and package directory.
RUN addgroup -S h-periodic && adduser -S -G h-periodic -h /var/lib/h-periodic h-periodic
WORKDIR /var/lib/h-periodic

COPY requirements/requirements.txt ./

RUN apk add build-base linux-headers

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001
USER h-periodic
CMD ["bin/init-env", "supervisord", "-c", "conf/supervisord.conf"]
