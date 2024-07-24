import cloudpickle
from . import quartznet

def get_config():
    cloudpickle.register_pickle_by_value(quartznet)

    return {'repo': 'jinensetpal/asr',
            'name': 'model',
            'version': '8',
            'post_hook': quartznet.post_hook,
            'pre_hook': quartznet.pre_hook,
            'label_config': quartznet.LABEL_CONFIG}
