from typing import List, Dict, Optional
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.response import ModelResponse

class DagsHubLSModel(LabelStudioMLBase):
    """Custom ML Backend model
    """

    def __init__(self):
        pass

    def configure(self, model, pre_hook, post_hook):
        self.model = model
        self.pre_hook = pre_hook
        self.post_hook = post_hook

    def setup(self):
        self.set("model_version", "0.0.1")

    def predict(self, tasks: List[Dict], context: Optional[Dict] = None, **kwargs) -> ModelResponse:
        tasks = [(self.ds['path'] == self.dp_map[self.dp_map['datapoint_id'] == task['meta']['datapoint_id']].iloc[0].path).head()[0].download_file().as_posix() for task in tasks] # get local path
        
        print(f'''\
        Run prediction on {tasks}
        Received context: {context}
        Project ID: {self.project_id}
        Label config: {self.label_config}
        Parsed JSON Label config: {self.parsed_label_config}
        Extra params: {self.extra_params}''')

        return ModelResponse(predictions=self.post_hook(self.model.predict(self.pre_hook(tasks))))
    
    def fit(self, event, data, **kwargs):
        pass
