import cloudpickle
from . import yolov8

def get_config():
    cloudpickle.register_pickle_by_value(yolov8)

    return {'repo': 'jinensetpal/COCO_1K',
            'name': 'yolov8-seg',
            'version': '1',
            'post_hook': yolov8.post_hook,
            'pre_hook': yolov8.pre_hook,
            'label_config': yolov8.LABEL_CONFIG}
