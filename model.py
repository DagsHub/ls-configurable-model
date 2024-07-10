import pickle
import pprint
from typing import List, Dict, Optional
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.response import ModelResponse

from label_studio_sdk.converter import brush
from uuid import uuid4
import torch
import json

COUNTER = 10

def post_hook(predictions):
    global COUNTER
    from uuid import uuid4
    results = []

    for prediction in list(predictions):
        result = []
        width, height = prediction.orig_shape
        for idx, (mask, label_idx) in enumerate(zip(prediction.masks, prediction.boxes.cls.cpu().tolist())):
            result.append({
                'id': COUNTER,
                'from_name': 'label',
                'to_name': 'image',
                'original_width': width,
                'original_height': height,
                'image_rotation': 0,
                'value': {
                    'closed': True,
                    'points': (prediction.masks.xyn[idx] * 100).astype(float).tolist(),
                    'polygonlabels': [prediction.names[label_idx]],
                },
                'type': 'polygonlabels',
                'readonly': False,
                'score': 1
                })
            COUNTER += 1
        results.append({'result': result, 'score': 1})
    return results

class DagsHubLSModel(LabelStudioMLBase):
    """Custom ML Backend model
    """

    def __init__(self):
        pass

    def configure(self, model, pre_hook, post_hook, ds, dp_map):
        self.model = model
        self.pre_hook = pre_hook
        self.post_hook = post_hook
        self.ds = ds
        self.dp_map = dp_map

    def setup(self):
        self.set("model_version", "0.0.1")

    def predict(self, tasks: List[Dict], context: Optional[Dict] = None, **kwargs) -> ModelResponse:
        print(tasks)
        tasks = [(self.ds['path'] == self.dp_map[self.dp_map['datapoint_id'] == task['meta']['datapoint_id']].iloc[0].path).head()[0].download_file().as_posix() for task in tasks] # get local path
        
        print(f'''\
        Run prediction on {tasks}
        Received context: {context}
        Project ID: {self.project_id}
        Label config: {self.label_config}
        Parsed JSON Label config: {self.parsed_label_config}
        Extra params: {self.extra_params}''')

        pickle.dump(tasks, open('tasks.pkl', 'wb'))
        pickle.dump(self.model.predict(self.pre_hook(tasks)), open('predictions.pkl', 'wb'))
        result = post_hook(self.model.predict(self.pre_hook(tasks)))
        pickle.dump(result, open('result.pkl', 'wb'))

        pprint.pprint(result)
        json.dump(result, open('result.json', 'w'))
        return result
    
    def fit(self, event, data, **kwargs):
        pass
