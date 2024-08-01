#!/usr/bin/env python3

from .easy_ocr import get_config
from . import easy_ocr
import cloudpickle

cloudpickle.register_pickle_by_value(easy_ocr)

__all__ = [get_config.__name__]
