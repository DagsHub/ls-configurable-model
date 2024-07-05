#!/usr/bin/env python3

from configurable_backend.model import DagsHubLSModel
from flask import Flask, request
import cloudpickle
import requests
import docker
import shutil

CURRENT_PORT = 9091

client = docker.from_env()
app = Flask(__name__)
portmap = {}

@app.post('/initialize')
def initialize_hooks():
    global CURRENT_PORT
    ## start a new instance of the image
    portmap[CURRENT_PORT] = client.containers.run('configurable-ls-backend', ports={f'9090/tcp': str(CURRENT_PORT)}, detach=True)
    ## configure the model
    requests.post(f'http://127.0.0.1:{CURRENT_PORT}/configure',
                  headers=request.headers,
                  json=request.json)
    CURRENT_PORT += 1
    ## return link
    return f'Port Forward: http://127.0.0.1:{CURRENT_PORT-1}/'
