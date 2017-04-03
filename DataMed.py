#!/usr/bin/python
# -*- coding: utf-8 -*-

"""""
https://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/
"""""
import re
import numpy as np
import os
from datetime import datetime 
import matplotlib.pyplot as plt 
import pandas as pd
import xlsxwriter


def plot_histograms( df , variables , n_rows , n_cols ):
    fig = plt.figure( figsize = ( 16 , 12 ) )
    for i, var_name in enumerate( variables ):
        ax=fig.add_subplot( n_rows , n_cols , i+1 )
        df[ var_name ].hist( bins=10 , ax=ax )
        ax.set_title( 'Skew: ' + str( round( float( df[ var_name ].skew() ) , ) ) ) # + ' ' + var_name ) #var_name+" Distribution")
        ax.set_xticklabels( [] , visible=False )
        ax.set_yticklabels( [] , visible=False )
    fig.tight_layout()  # Improves appearance a bit.
    plt.show()


def plot_categories( df , cat , target , **kwargs ):
    row = kwargs.get( 'row' , None )
    col = kwargs.get( 'col' , None )
    facet = sns.FacetGrid( df , row = row , col = col )
    facet.map( sns.barplot , cat , target )
    facet.add_legend()

root = '/Users/mrouer/médecine/Chirurgie/Vasculaire/Publications/LDN learning curve/'
excel =  "data_rein" 

###create a folder with all newly created files
folder_name=excel+'_description'
folder_path=root+folder_name
if not os.path.exists(folder_path):
    os.mkdir(folder_path)


#first check if there is a csv file with df previously exported...
if os.path.isfile(folder_path+'/'+excel+'.csv') == True:
    df = pd.read_csv(folder_path+'/'+excel+'.csv', encoding = 'utf8') #sometimes some people would prefer encoding in 'cp1252'
else:
    #df = pd.read_csv('out.csv')
    df = pd.read_excel(open(root+excel+'.xlsx','rb'), sheetname='datas')


#Lower-case all DataFrame column names
#df.columns = map(df.columns.str.lower(), df.columns)    

print(df.dtypes)
print (df.shape)
#print (df.head(0))	


#generate box plot for all datas
#pd.options.display.mpl_style = 'default'
#df.boxplot()

replace_y = [r"\boui\b", r"\by\b", r"\yes\b"]
replace_n = [r"\bnon\b", r"\bn\b", r"\no\b"]

#object var
for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == 'object': # Only apply for columns with categorical strings
         if len(df[feature].unique()) <=6 : #select only objects with no more than 6 different values to avoir 'comments' columns
               df[feature] = df[feature].str.lower()
               print (feature, df[feature].unique()) #print before transformation
               df[feature] = df[feature].replace(replace_n, 0, regex=True)
               df[feature] = df[feature].replace(replace_y, 1, regex=True)
               
               #check if replace worked !
               if all(x in df[feature].unique() for x in [0,1]) == True:
                   print ('success: ', feature, df[feature].unique()) #print after transformation if applicable
                #print number of each individual value
               print df[feature].value_counts()
        
#binary var
for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == 'float64' or df[feature].dtype == 'int64': # Only apply for columns with categorical strings
         if len(df[feature].unique()) <=6 : #select only objects with a little different var
               print (feature, df[feature].unique())
               print df[feature].value_counts()

#print (df.describe()) #description af all continuous variables
describe = df.describe(include='all')
describe.to_csv(folder_path+'/descriptif.csv', encoding = 'utf8')       


#export newly created df in a csv and/or xls file according to anyone for later analysis

if 'index' not in df:
    df = df.reset_index()
#if os.path.isfile(folder_path+'/'+excel+'.csv') == False: ###if you don't want to replace csv file
df.to_csv(folder_path+'/'+excel+'.csv', index=False, encoding = 'utf8')      

#if os.path.isfile(folder_path+'/'+excel+'.xlsx') == False: ###if you don't want to replace xls file
writer = pd.ExcelWriter(folder_path+'/'+excel+'.xlsx', engine = 'xlsxwriter')
df.to_excel(writer, sheet_name = 'sheet1')
writer.save()

   
