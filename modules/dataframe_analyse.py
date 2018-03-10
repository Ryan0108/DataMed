#!/usr/bin/python
# -*- coding: utf-8 -*-

"""""
Useful links

https://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/

We assume that all the data are in one sheet in a single excel file. You can parse and modify this script
to gather or create multiple sheets...


"""""
from datetime import datetime 
import datetime
import numpy as np


#timer for time processing analysis
from .timer import *

@time_all_class_methods
class analyseDataFrame:
    def __init__(self, df):
        self.df = df
#        self.binary_types = ['float64', 'float32', 'int64', 'int32']
#        self.continuous_types = ['float64', 'float32', 'int64', 'int32']
        self.numbers = [np.float, np.int]
        
    def data_type(self):
        datatype_dict = {}
        for col_name in self.df.columns:
            if self.df[col_name].dtype in self.numbers: # Only apply for columns with categorical strings
                if (self.df[col_name].nunique()) == 2 : #only 2 values in the col
                   datatype_dict[col_name] = 'binary'
                elif 2 < (self.df[col_name].nunique()) <= 6 : #only 2 to 6 values in the col
                    datatype_dict[col_name] = 'categorical'
                elif (self.df[col_name].nunique()) > 6 :
                    datatype_dict[col_name] = 'continuous'
                ##situation where there is only 0 or 1 value
                else: 
                    datatype_dict[col_name] = 'single'
                         
            else:
                if (self.df[col_name].nunique()) == 2 : #only 2 values in the col
                   datatype_dict[col_name] = 'binary'
                elif 2 < (self.df[col_name].nunique()) <= 6 : #only 2 to 6 values in the col
                    datatype_dict[col_name] = 'categorical'
                else:
                    datatype_dict[col_name] = 'objec'
        
        return datatype_dict
                
    
    ###useless methods, kept just in case...
    def data(self):
        binary = []
        for col_name in self.df.columns:
            if self.df[col_name].dtype in self.numbers: # Only apply for columns with categorical strings
                if (self.df[col_name].nunique()) == 2 : #only 2 values in the col
                    binary.append(col_name)
        
        return binary   
    
    def cat(self):
        cat = []
        for col_name in self.df.columns:
            if self.df[col_name].dtype in self.numbers: # Only apply for columns with numeric values
                if 2 < (self.df[col_name].nunique()) <= 6 : #only 2 values in the col
                    cat.append(col_name)
        return cat
    
    def continuous(self):
        continuous = []
        for col_name in self.df.columns:
            if self.df[col_name].dtype == np.float64 or self.df[col_name].dtype == np.int: # Only apply for columns with categorical strings
                if (self.df[col_name].nunique()) >= 6 : #only 2 values in the col
                    continuous.append(col_name)
        return continuous
    
    #####
