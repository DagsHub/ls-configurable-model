from .yolov8_det import get_config
from . import yolov8_det
import cloudpickle

cloudpickle.register_pickle_by_value(yolov8_det)

__all__ = [get_config.__name__]
