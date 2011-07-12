#! /usr/bin/env python
# log.py

import os
import logging
import logging.config

logging.config.fileConfig(os.path.dirname(__file__) + '/conf/logging.conf')
