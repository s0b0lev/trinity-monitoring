#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

entry_point = 'monitoring=monitoring:MonitoringPlugin'

setup(
    name='trinity-monitoring',
    py_modules=['monitoring'],
    entry_points={
        'trinity.plugins': entry_point,
    },
)
