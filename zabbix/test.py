#!/usr/bin/env python

import fnmatch
import os
for file in os.listdir('/var/log/'):
    if fnmatch.fnmatch(file, '*.log'):
        print file
