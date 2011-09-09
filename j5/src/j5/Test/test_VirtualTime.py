#!/usr/bin/env python

from j5.Test import VirtualTime
from j5.OS import datetime_tz
import datetime
import time
import pickle
import os
import subprocess
import sys

def outside(code_str, *import_modules):
    """Runs a code string in a separate process, pickles the result, and returns it"""
    import_modules_str = 'import %s' % ', '.join(import_modules) if import_modules else ''
    command_string = 'import sys, pickle; sys.path = pickle.loads(sys.stdin.read()); %s; sys.stdout.write(pickle.dumps(%s))' % (import_modules_str, code_str)
    pickle_path = pickle.dumps(sys.path)
    p = subprocess.Popen([sys.executable, "-c", command_string], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ)
    results, errors = p.communicate(pickle_path)
    if errors and errors.strip():
        raise ValueError(errors)
    return pickle.loads(results)

def test_real_time():
    """tests that real time is still happening in the time module"""
    first_time = time.time()
    outside_time = outside("time.time()", "time")
    second_time = time.time()
    assert first_time < outside_time < second_time

def test_real_datetime_now():
    """tests that real time is still happening in the datetime module"""
    first_time = datetime.datetime.now()
    outside_time = outside("datetime.datetime.now()", "datetime")
    second_time = datetime.datetime.now()
    assert first_time < outside_time < second_time

def test_real_datetime_tz_now():
    """tests that real time is still happening in the datetime_tz module"""
    first_time = datetime_tz.datetime_tz.now()
    outside_time = outside("j5.OS.datetime_tz.datetime_tz.now()", "j5.OS.datetime_tz")
    second_time = datetime_tz.datetime_tz.now()
    assert first_time < outside_time < second_time

def test_virtual_time():
    """tests that we can set time"""
    first_time = time.time()
    VirtualTime.set_time(first_time + 100)
    late_time = time.time()
    VirtualTime.set_time(first_time - 100)
    early_time = time.time()
    VirtualTime.real_time()
    last_time = time.time()
    assert early_time < first_time < last_time < late_time

def test_virtual_datetime():
    """tests that setting time and datetime are both possible"""
    first_time = datetime.datetime.now()
    VirtualTime.set_time(VirtualTime.datetime_to_time(first_time) + 100)
    late_time = datetime.datetime.now()
    VirtualTime.set_time(VirtualTime.datetime_to_time(first_time) - 100)
    early_time = datetime.datetime.now()
    VirtualTime.real_time()
    last_time = datetime.datetime.now()
    assert early_time < first_time < last_time < late_time

def test_virtual_datetime_tz():
    """tests that setting time and datetime are both possible"""
    first_time = datetime_tz.datetime_tz.now()
    VirtualTime.set_time(VirtualTime.datetime_to_time(first_time) + 100)
    late_time = datetime_tz.datetime_tz.now()
    VirtualTime.set_time(VirtualTime.datetime_to_time(first_time) - 100)
    early_time = datetime_tz.datetime_tz.now()
    VirtualTime.real_time()
    last_time = datetime_tz.datetime_tz.now()
    assert early_time < first_time < last_time < late_time


