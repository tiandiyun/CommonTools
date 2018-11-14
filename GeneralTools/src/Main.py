# -*- coding:utf8 -*-

import sys
sys.path.append(sys.path[0])

from Test.TestArgparse import TestArgparse


if __name__ == "__main__":

    if len(sys.argv) < 1:
        sys.exit(0)

    cmd = sys.argv[1]
    del sys.argv[1]

    if cmd == 'Test':
        TestArgparse()
