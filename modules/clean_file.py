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
import matplotlib.pyplot as plt 
import pandas as pd
import xlsxwriter

#txt processing/remove accents
import unicodedata

#timer for time processing analysis
from .timer import *

#####Column names and blank values
def clean_name(col_name):
    #Lower-case all DataFrame column names
    col_name = col_name.lower()
    #strip columns titles
    col_name = col_name.strip()
    #replace accents for series titles
    ###Python 2.7
    #df.columns = [unicodedata.normalize('NFKD', unicode(col)).encode('ASCII', 'ignore') for col in df.columns]
    ###Python 3.6
    col_name = unicodedata.normalize('NFKD', col_name).encode('ASCII', 'ignore').decode('utf_8')
    col_name = re.sub(r'[^\w\s]',' ',col_name)
    
    #replace all "'", "d", "l"..., by _
    links = "l d de la le the"
    links = links.split()
    for l in links:
        col_name = re.sub(r'\s'+l+'\s','_',col_name)
    
    #replace spaces
    col_name = re.sub(r'\s','_',col_name)
    
    return col_name


@time_all_class_methods
class cleanFile:  
    def __init__(self, df):
        #remove empty columns
        self.df = df.dropna(axis='columns', how='all')

    #####Column names and blank values
    def column_names(self):
        df = self.df
        df.columns = [clean_name(col) for col in df.columns]
            
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
        replace_nan = [r"\bNAN\b", r"\bnan\b", r"\bNaN\b"]
        
        for name in self.df.columns:
            self.df[name] = self.df[name].replace(replace_n, float(0), regex=True)
            self.df[name] = self.df[name].replace(replace_y, float(1), regex=True)
            self.df[name] = self.df[name].replace(replace_nan, "Nan", regex=True)
        
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
        
                
class ExcelFormatting(object):
    
    def __init__(self, sheet, writer): #load path to excel file and worksheet
        
        self.worksheet = sheet
        self.writer = writer
        
    def column_width(self):
            
        #1/ Convert sheet into a panda dataframe
        df=pd.read_excel('descriptif.xlsx', sheetname=self.worksheet.get_name(), encoding = 'utf8')
        
        worksheet_writer = self.writer.sheets[self.worksheet.get_name()]

        #2/get max width of each column
        #http://stackoverflow.com/questions/34757703/how-to-get-the-longest-length-string-integer-float-from-a-pandas-column-when-the/34757855#34757855
        for i, j in enumerate (df.columns):

            #1/ get the max length of the describe series
            field_length = df[j].astype(str).map(len)
            max_length = df.loc[field_length.argmax(), j]   
            #combine title len and max length of the series, get the highest value to define the column width
            max_larg = [len(str(max_length)), len(j)]

            worksheet_writer.set_column(i+1,i+1, max(max_larg), None)
            worksheet_writer.set_column(0,0,20, None)

