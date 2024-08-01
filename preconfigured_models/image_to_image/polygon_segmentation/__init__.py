from .yolov8 import get_config
from . import yolov8
import cloudpickle

cloudpickle.register_pickle_by_value(yolov8)

__all__ = [get_config.__name__]
