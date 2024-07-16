#!/usr/bin/env python3

from model import DagsHubLSModel
from flask import Flask, request
import cloudpickle
import requests
import docker
import shutil
import time

CURRENT_PORT = 9091

client = docker.from_env()
app = Flask(__name__)
portmap = {}

@app.post('/configure')
def initialize_hooks():
    global CURRENT_PORT
    ## start a new instance of the image
    portmap[CURRENT_PORT] = client.containers.run('configurable-ls-backend', ports={f'9090/tcp': str(9091)}, detach=True)
    time.sleep(10)
    ## configure the model
    requests.post(f'http://127.0.0.1:{CURRENT_PORT}/configure',
                  headers=request.headers,
                  json=request.json)
    CURRENT_PORT += 1
    ## return link
    return f'Port Forward: http://127.0.0.1:{CURRENT_PORT - 1}/'
