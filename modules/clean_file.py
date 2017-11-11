#!/usr/bin/python
# -*- coding: utf-8 -*-

"""""
Useful links

https://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/

We assume that all the data are in one sheet in a single excel file. You can parse and modify this script
to gather or create multiple sheets...


"""""
import re
import numpy as np
import os
from datetime import datetime 
import datetime
import matplotlib.pyplot as plt 
import pandas as pd
import xlsxwriter
#txt processing/remove accents
import unicodedata

#timer for time processing analysis
from .timer import *


@time_all_class_methods
class cleanFile:  
    def __init__(self, df):
        #remove empty columns
        self.df = df.dropna(axis='columns', how='all')

    #####Column names and blank values
#    @fn_timer
    def column_names(self):
        df = self.df
        #Lower-case all DataFrame column names
        df.columns = [col.lower() for col in df.columns]
        #strip columns titles
        df.columns = [col.strip() for col in df.columns]
        #replace accents for series titles
        ###Python 2.7
        #df.columns = [unicodedata.normalize('NFKD', unicode(col)).encode('ASCII', 'ignore') for col in df.columns]
        ###Python 3.6
        df.columns = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf_8') for col in df.columns]
        df.columns = [re.sub(r'[^\w\s]',' ',col) for col in df.columns]

        #replace all "'", "d", "l"..., by _
        links = "l d de la le the"
        links = links.split()
        for l in links:
            df.columns = [re.sub(r'\s'+l+'\s','_',col) for col in df.columns]
        #replace spaces
        df.columns = [re.sub(r'\s','_',col) for col in df.columns]
        #Check if there is date columns which are read as objects
        #http://stackoverflow.com/questions/33204500/pandas-automatically-detect-date-columns-at-run-time
        df = df.apply(lambda col: pd.to_datetime(col, errors = 'ignore')
                      if col.dtypes == object
                      else col,
                      axis = 0)
        return df
    
#    @fn_timer
    def replace_binary(self):
        replace_y = [r"\boui\b", r"\by\b", r"\byes\b", r"\bYES\b", r"\bY\b", r"\bOUI\b", r"\bO\b", r"\bOUI\b"]
        replace_n = [r"\bnon\b", r"\bn\b", r"\bno\b", r"\bNO\b", r"\bN\b", r"\bNON\b"]
        
        for name in self.df.columns:
            self.df[name] = self.df[name].replace(replace_n, 0, regex=True)
            self.df[name] = self.df[name].replace(replace_y, 1, regex=True)
        
        return self.df
    
#    @fn_timer
    def column_data(self):
        #replace accents
        ##http://stackoverflow.com/questions/37926248/how-to-remove-accents-from-values-in-columns
        #cols = df.select_dtypes(include = [np.object]).columns
        #df[cols] = df[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))
        
        #replace blank values  
        self.df.replace(r'\s+( +\.)|#',np.nan,regex=True).replace('',np.nan)
        
#       self.df[name] = self.df[name].str.lower() -> replace int
