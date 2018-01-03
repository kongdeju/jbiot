# -*- coding: utf-8 -*-
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'

from subjobs.splitcmd import *
from subjobs.lsub import *
from subjobs.csub import *


