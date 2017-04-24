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

#def remove_accents(data):
#    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

def plot_histograms_continuous( df, variables, n_rows, n_cols ):
    fig = plt.figure( figsize = ( 16 , 12 ) )
    for i, var_name in enumerate( variables ):
        ax=fig.add_subplot( n_rows , n_cols , i+1 )
        df[ var_name ].hist( bins=10 , ax=ax )
        ax.set_title( 'Skew: ' + str( round( float( df[ var_name ].skew() ) , ) ) ) # + ' ' + var_name ) #var_name+" Distribution")
        ax.set_xticklabels( [] , visible=False )
        ax.set_yticklabels( [] , visible=False )
    #select min max values for x and y axis
    xmin, xmax, ymin, ymax = df.min, df.max, 0, 100 #consider Y axis in percentage
    plt.axis([xmin, xmax, ymin, ymax])
    fig.tight_layout()  # Improves appearance a bit.
    plt.show()

"""""
Complete the following informations 
path to the file
name of the file
name of the sheets in the excel file
If you don't know how: place the python script in the same folder as the excel file, and set root by nothin ("")
"""""


root = '/Users/mrouer/médecine/Chirurgie/Vasculaire/Publications/LDN learning curve/' 
excel =  "data_rein" 
sheet = "name or list"


###create a folder with all newly created files 
folder_name=excel+'_description'
folder_path=root+folder_name
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    os.mkdir(folder_path+'/data')
    os.mkdir(folder_path+'/graph')

#first check if there is a csv file with df previously exported...
if os.path.isfile(folder_path+'/data/'+excel+'.csv') == True:
    df = pd.read_csv(folder_path+'/data/'+excel+'.csv', encoding = 'utf8') #sometimes some people would prefer encoding in 'cp1252'
else:
    #df = pd.read_csv('out.csv')
    df = pd.read_excel(open(root+excel+'.xlsx','rb'), sheetname=sheet)


#define groups =>list
target_list = ["target"] #change the name according to the grouping column
#if target_column in df:
#    df["target"] = df[target_column]
#    #set target column in N°2 place after index
#    ####to be done


#Lower-case all DataFrame column names
df.columns = [col.lower() for col in df.columns]
#replace accents
df.columns = [unicodedata.normalize('NFKD', unicode(col)).encode('ASCII', 'ignore') for col in df.columns]
#replace all "'", "d", "l", by _
df.columns = [re.sub(r'[^\w\s]',' ',col) for col in df.columns]
links = "l d de la le the"
df.columns = [re.sub(r'\sl\s','_',col) for col in df.columns]
#replace spaces
df.columns = [re.sub(r'\s','_',col) for col in df.columns]

#remove empty columns
df = df.dropna(axis='columns', how='all')

#replace blank values  
"""""
http://stackoverflow.com/questions/30392720/pandas-dataframe-replace-blanks-with-nan
if you want to replace Nan values by another string: df = df.fillna('string')
http://pandas.pydata.org/pandas-docs/stable/missing_data.html
"""""
df.replace(r'\s+( +\.)|#',np.nan,regex=True).replace('',np.nan)

print df.columns
print(df.dtypes)
print (df.shape)
#print (df.head(0))	


replace_y = [r"\boui\b", r"\by\b", r"\yes\b"]
replace_n = [r"\bnon\b", r"\bn\b", r"\no\b"]

#create excel file to save all descriptive datas
writer_descriptive = pd.ExcelWriter(folder_path+'/descriptif.xlsx', engine = 'xlsxwriter')
row = 0 #row to start writing the tabs in the excel file

""""
Generate descriptives data and write them in an excel file
"""""

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
#               print df[feature].value_counts()
#               print ('in percent: ' , df[feature].value_counts(normalize=True))
               
#               generate tables with statistics 
               tab = pd.crosstab(index = df[feature], columns = "count")
#               convert in percents
#               tab = (tab/tab.sum())*100
               tab.to_excel(writer_descriptive, sheet_name = 'tabs', startrow = row)
#               translate tables downards
                          
               if len(target_list) >0 :
                   for target in target_list:
                       #write raw numbers
                       tab = pd.crosstab(index = df[feature], columns = df[target], margins=True)
                       tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = 3, startrow = row)
                       #write in percent
                       tab = pd.crosstab(index = df[feature], columns = df[target], normalize = 'all', margins=True)
                       tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = 10, startrow = row)
                       #translate tables downards
                       row = row + df[feature].nunique() + 3
               else:
                   row = row + df[feature].nunique() + 2
                                 
#binary and categorical var
for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == np.float or df[feature].dtype == np.int: # Only apply for columns with categorical strings
         if len(df[feature].unique()) <=6 : #select only objects with a little different var
               
         #generate tables with statistics 
               tab = pd.crosstab(index = df[feature], columns = "count")
#               convert in percents
#               tab = (tab/tab.sum())*100
               tab.to_excel(writer_descriptive, sheet_name = 'tabs', startrow = row)
#               translate tables downards
                          
               if len(target_list) > 0:
                   for t in target_list:
                       if df[t].name is not df[feature].name: #don't include the chosen group columns, otherwise it throws an error
                           #write raw numbers
                           tab = pd.crosstab(index = df[feature], columns = df[t], margins=True)
                           tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = 3, startrow = row)
                           #write in percent
                           tab = pd.crosstab(index = df[feature], columns = df[t], normalize = 'all', margins=True)
                           tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = 10, startrow = row)
                           #translate tables downards
                           row = row + df[feature].nunique() + 3
               else:
                   row = row + df[feature].nunique() + 2

#Continuous variables
for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == np.float or df[feature].dtype == np.int: # Only apply for columns with categorical strings
         if len(df[feature].unique()) >=6 : #select only objects with a little different var
               if len(target_list) > 0:
                   for t in target_list:
                       if df[t].name is not df[feature].name: #don't include the chosen group columns, otherwise it throws an error
                           #write raw numbers
                           tab = df[feature].groupby(df[t]).describe()
                           #convert tab to a frame to write it in the excel file
                           tab.to_frame(name=feature).to_excel(writer_descriptive, sheet_name = 'tabs', startcol = 1, startrow = row)                           
                           #translate tables downards
                           row = row + df[feature].nunique() + 3
               else:
                   row = row + df[feature].nunique() + 2



"""""
Create graph visualization 
"""""

#binary var
pd.options.display.mpl_style = 'default'
#adjust layout size
#wide = 1
#length = 1+len((df.select_dtypes(include=[np.float])).columns)/wide
#df.select_dtypes(include=[np.float]).plot(kind='box', subplots=True, figsize = (length*10,10), layout=(length, wide) )
#plt.tight_layout()

cols = df.columns.tolist()
if 'index' in cols:
    cols.remove(u'index') #remove index column

for feature in cols: # Loop through all columns in the dataframe
    if df[feature].dtype == np.float or df[feature].dtype == np.int:
#        df[feature].plot(kind='box', grid=True, ) 
#       Another way to generate boxplot
        df.boxplot(column = feature,  grid=True, )
        plt.savefig(folder_path+'/graph/'+feature+'_boxplot.png', bbox_inches='tight')
        plt.show()
        ax = df[feature].plot.hist(grid=True,normed=True)
        ax.set_xlabel(feature)
        plt.savefig(folder_path+'/graph/'+feature+'_hist.png', bbox_inches='tight')
        plt.show()
        
        #groupBy...
        if len(target_list) > 0:
                   for t in target_list:
                       if df[t].name is not df[feature].name: #don't include the chosen group columns, otherwise it throws an error
                            df.boxplot(column = feature, by = df[t], grid=True)
                            plt.savefig(folder_path+'/graph/'+feature+'_'+t+'_boxplot.png', bbox_inches='tight')
                            plt.show()

                            df.hist(column = feature, by = df[t], grid=True)
                            plt.suptitle(feature)
                            plt.savefig(folder_path+'/graph/'+feature+'_'+t+'_hist.png', bbox_inches='tight')
                            plt.show()


#print (df.describe()) #description af all continuous variables
describe = df.describe(include='all')
describe.to_csv(folder_path+'/descriptif.csv', encoding = 'utf8')       
#write in an excel file
#writer_descriptive = pd.ExcelWriter(folder_path+'/descriptif.xlsx', engine = 'xlsxwriter')
describe.to_excel(writer_descriptive, sheet_name = 'descriptif')
writer_descriptive.save()

#export newly created df in a csv and/or xls file according to anyone for later analysis
if 'index' not in df:
    df = df.reset_index()
#if os.path.isfile(folder_path+'/'+excel+'.csv') == False: ###if you don't want to replace csv file
df.to_csv(folder_path+'/data/'+excel+'.csv', index=False, encoding = 'utf8')      

#if os.path.isfile(folder_path+'/'+excel+'.xlsx') == False: ###if you don't want to replace xls file
writer_df = pd.ExcelWriter(folder_path+'/data/'+excel+'.xlsx', engine = 'xlsxwriter')
df.to_excel(writer_df, sheet_name = 'sheet1')
writer_df.save()



