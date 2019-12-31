# -*- coding: utf-8 -*-
# MLToolkit (mltk)

__docformat__ = 'restructuredtext'
__name__="mltk"
__distname__="pymltoolkit"
__version__="0.1.8"
__description__= 'End-to-end Machine Learning Toolkit (MLToolkit/mltk) for Python'
__author__="Sumudu Tennakoon"
__url__="https://mltoolkit.github.io/MLToolKit"
__create_date__="Sun Jul 01 2018"
__last_update__="Sat Sap 28 2019"
__license__="""
Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""
__doc__="""
MLToolkit - a verstile helping library for machine learning
===========================================================
'MLToolkit' is a Python package providing a set of user-friendly functions to 
help building machine learning models in data science research or production 
focused projects. It is compatible with and interoperate with popular data 
analysis, manipulation and machine learning libraries Pandas, Sci-kit Learn, 
Tensorflow, Statmodels, Catboost, XGboost, etc.

Main Features
-------------
- Data Extraction (SQL, Flatfiles, etc.)
- Exploratory data analysis (statistical summary, univariate analysis, etc.)
- Feature Extraction and Engineering
- Model performance analysis and comparison between models
- Cross Validation and Hyper parameter tuning
- JSON input script for executing model building and scoring tasks.
- Model Building UI
- Auto ML (automated machine learning)
- Model Deploymet and Serving via RESTful  API

Author
------
- Sumudu Tennakoon

Links
-----
Website: http://sumudu.tennakoon.net/projects/MLToolkit
Github: https://github.com/mltoolkit/MLToolKit

License
-------
Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

hard_dependencies = ('numpy', 'scipy', 'matplotlib', 'pandas','sklearn', 'statsmodels') #,'re', 'tensorflow', 'catboost') #'tensorflow'
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Following packages are required but missing in the Python distribution: {}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies

from datetime import datetime
import gc
import traceback
import gc
import os
from timeit import default_timer as timer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings
warnings.filterwarnings("ignore")

# Package scripts
from mltk.etl import *
from mltk.string import *
from mltk.explore import *
from mltk.model import *
from mltk.matrics import *
from mltk.deploy import *
from mltk.modelchest import *
from mltk.project import *

print('mltk=={}'.format(__version__.strip()))
###############################################################################
#                           SET DISPLAY ENVIRONMENT                           #
###############################################################################
pd.set_option("display.max_columns",1000)
pd.set_option("display.max_rows",500)
pd.set_option('expand_frame_repr', False)
pd.set_option('large_repr', 'truncate')
pd.set_option('precision', 5)
###############################################################################