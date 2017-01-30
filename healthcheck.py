# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os

import kombu
from flask import Flask, jsonify

app = Flask(__name__)


class BrokerConnectionError(Exception):
    pass


@app.route('/_status')
def status():
    connection = kombu.Connection(os.environ['BROKER_URL'])
    try:
        connection.connect()
    finally:
        connection.close()

    return jsonify({'status': 'ok'})


@app.errorhandler(500)
def error(error):
    app.logger.error(error)
    return jsonify({'status': 'error', 'reason': repr(error)}), 500


if __name__ == "__main__":
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.ERROR)

    app.run('0.0.0.0', os.getenv('PORT', 8080))
