import cloudpickle
import requests
import base64
import json

URL = 'http://127.0.0.1:5000/'

# example request
resp = requests.post(f'{URL}/initialize',
                     headers = {'Content-Type': 'application/json'},
                     json=json.dumps({'host': 'dagshub.com',
                                      'username': 'jinensetpal',
                                      'repo': 'COCO_1K',
                                      'model': 'yolov8-seg',
                                      'version': 'latest',
                                      'datasource_repo': 'jinensetpal/COCO_1K',
                                      'datasource_name': 'COCO_1K',
                                      'pre_hook': base64.b64encode(cloudpickle.dumps(lambda x: x)).decode("utf-8"),
                                      'post_hook': base64.b64encode(cloudpickle.dumps(lambda x: x)).decode("utf-8")}))
