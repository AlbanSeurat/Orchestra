#!/usr/bin/python
import logging
import sys
from orchestra.orchestra import Orchestra

#logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(asctime)s %(name)-24s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

main = Orchestra(sys.argv[1], sys.argv[2])

main.startup()





