#!/usr/bin/env python

import sys
import threading
import types
import time
import datetime as datetime_module
# from j5.OS import datetime_tz as datetime_tz_module

_time_lock = threading.RLock()
_time_offset = 0

_original_time = time.time

def _virtual_time():
    """Overlayed form of time.time() that adds _time_offset"""
    return _original_time() + _time_offset

time.time = _virtual_time

_original_datetime_module = datetime_module
_original_datetime_type = _original_datetime_module.datetime
_original_datetime_now = _original_datetime_type.now
_original_datetime_utcnow = _original_datetime_type.utcnow

_virtual_datetime_attrs = dict(_original_datetime_type.__dict__.items())
class datetime(_original_datetime_module.datetime):
    def __new__(cls, *args, **kwargs):
        dt = super(_virtual_datetime_type, cls).__new__(cls, *args, **kwargs)
        newargs = list(dt.timetuple()[0:6])+[dt.microsecond, dt.tzinfo]
        return _original_datetime_type.__new__(cls, *newargs)

    @classmethod
    def now(cls):
        """Virtualized datetime.datetime.now()"""
        dt = super(_virtual_datetime_type, cls).now() + _original_datetime_module.timedelta(seconds=_time_offset)
        newargs = list(dt.timetuple()[0:6])+[dt.microsecond, dt.tzinfo]
        return _original_datetime_type.__new__(cls, *newargs)

    @classmethod
    def utcnow(cls):
        """Virtualized datetime.datetime.utcnow()"""
        dt = super(_virtual_datetime_type, cls).utcnow() + _original_datetime_module.timedelta(seconds=_time_offset)
        newargs = list(dt.timetuple()[0:6])+[dt.microsecond, dt.tzinfo]
        return _original_datetime_type.__new__(cls, *newargs)

_virtual_datetime_type = datetime
_original_datetime_module.datetime = _virtual_datetime_type

def datetime_to_time(dt):
    """converts a datetime object to a local time float"""
    return time.mktime(dt.timetuple()) + dt.microsecond * 0.000001

def set_time(new_time):
    """Sets the current time to the given time.time()-equivalent value"""
    global _time_offset
    _time_lock.acquire()
    try:
        _time_offset = new_time - _original_time()
    finally:
        _time_lock.release()

def real_time():
    """Reverts to real time operation"""
    global _time_offset
    _time_lock.acquire()
    try:
        _time_offset = 0
    finally:
        _time_lock.release()


