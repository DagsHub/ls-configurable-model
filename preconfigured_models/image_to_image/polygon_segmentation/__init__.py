from .yolov8_seg import get_config
from . import yolov8_seg
import cloudpickle

cloudpickle.register_pickle_by_value(yolov8_seg)

__all__ = [get_config.__name__]
