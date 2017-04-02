#!/usr/bin/python
# -*- coding: utf-8 -*-

"""""
https://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/
"""""
import numpy as np
import os
from datetime import datetime 
import matplotlib.pyplot as plt 
import pandas as pd


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

root = 'path to folder'
excel =  "data_rein" 
#df = pd.read_csv('out.csv')
df = pd.read_excel(open(root+excel+'.xlsx','rb'), sheetname='datas')
#Create a folder with result of all descriptive variables

Folder_name=excel+'_description'
folder_path=root+Folder_name
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    
print(df.dtypes)
print (df.shape)
print (df.head(0))	
print (df.describe()) #description af all continuous variables
describe = df.describe()
describe.to_csv(folder_path+'descriptif.csv')

#generate box plot for all datas
pd.options.display.mpl_style = 'default'
df.boxplot()

#object var
for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == 'object': # Only apply for columns with categorical strings
         if len(df[feature].unique()) <=6 : #select only objects with a little different var
               df[feature] = df[feature].str.lower()
               print (feature, df[feature].unique())
               print df[feature].value_counts()
        
#binary var
for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == 'float64': # Only apply for columns with categorical strings
         if len(df[feature].unique()) <=6 : #select only objects with a little different var
               print (feature, df[feature].unique())
               print df[feature].value_counts()
               
    
