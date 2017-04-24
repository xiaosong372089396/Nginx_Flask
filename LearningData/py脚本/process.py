#!/usr/bin/env python

import os

process = os.popen("ps aux | grep 'XL' | awk '{print $3}' | cut -f 1 -d '.'").read().strip('\n').split('\n')
process.reverse()
a = int(max(process))
print a
