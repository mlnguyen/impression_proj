#!/usr/bin/env python3

# STEP 4 --------------------------------------------------
# Make figures for evaluating fieldmap correction and motion
# during scans.
# --------------------------------------------------------

# python imports
from os import listdir, makedirs
from os.path import isfile, join, exists
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from nilearn import image, plotting
