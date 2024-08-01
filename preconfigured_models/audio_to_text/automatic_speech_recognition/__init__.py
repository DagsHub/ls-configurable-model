#!/usr/bin/env python3

from .quartznet import get_config
from . import quartznet
import cloudpickle

cloudpickle.register_pickle_by_value(quartznet)

__all__ = [get_config.__name__]
