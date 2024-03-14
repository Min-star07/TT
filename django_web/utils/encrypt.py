# -*- coding: utf-8 -*-

"""
@author: Min Li
@e-mail: limin93@ihep.ac.cn
@file: encrypt.py
@time: 2023/11/25 22:41
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hashlib
from django.conf import settings
def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()