#!/bin/sh

if [ ! -n "$BROKER_URL" ]; then
  echo "ERROR: BROKER_URL environment variable needs to be set."
  exit 1
fi

supervisord -c supervisord.conf
