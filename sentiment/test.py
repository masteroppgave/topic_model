import numpy as numpy
import pandas as pd
import dill


with open("clf.dill", "rb") as fid:
	loaded = dill.load(fid)
