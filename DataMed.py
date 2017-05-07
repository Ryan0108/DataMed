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

"""""
Complete the following informations 
-path to the file
-name of the file
-name of the sheets in the excel file
If you don't know how: place the python script in the same folder as the excel file, and set root by nothin ("")
"""""

#####
#####1/path and folder name informations to fill !!!
#####
root = 'root_to_folder' 
excel_full =  "name_of_excel_file.extension" 
#sheet = "sheet_name" #by default, first sheet is read
excel_name = (excel_full.split("."))[0] #take only the name without extension
target_list = [] #list each target group separated by a coma with "" =>["target1", "target2"...]


###create a folder with all newly created files 
folder_name=excel_name+'_description'
folder_path=root+folder_name
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    os.mkdir(folder_path+'/data')
    os.mkdir(folder_path+'/graph')

#first check if there is a clean csv file previously generated...
if os.path.isfile(folder_path+'/data/'+excel_name+'.csv') == True:
    df = pd.read_csv(folder_path+'/data/'+excel_name+'.csv', encoding = 'utf8') #sometimes some people would prefer encoding in 'cp1252'
else:
    #df = pd.read_csv('out.csv')
    df = pd.read_excel(open(root+excel_name,'rb'))


#####
#####2/ create excel files to save data
#create excel file to save all descriptive datas
writer_descriptive = pd.ExcelWriter(folder_path+'/descriptif.xlsx', 
                                    engine = 'xlsxwriter', 
                                    default_date_format = 'dd/mm/yyyy', #change date format according to your preferences
                                    ) 
workbook_descriptive = writer_descriptive.book

#####
#####3/"clean" file
#####

#remove empty columns
df = df.dropna(axis='columns', how='all')

#####Column names


#Lower-case all DataFrame column names
df.columns = [col.lower() for col in df.columns]
#strip columns titles
df.columns = [col.strip() for col in df.columns]
#replace accents for series titles
df.columns = [unicodedata.normalize('NFKD', unicode(col)).encode('ASCII', 'ignore') for col in df.columns]
df.columns = [re.sub(r'[^\w\s]',' ',col) for col in df.columns]

#replace all "'", "d", "l"..., by _
links = "l d de la le the"
links = links.split()
for l in links:
    df.columns = [re.sub(r'\s'+l+'\s','_',col) for col in df.columns]
#replace spaces
df.columns = [re.sub(r'\s','_',col) for col in df.columns]

#####series

#Check if there is date columns which are read as objects
#http://stackoverflow.com/questions/33204500/pandas-automatically-detect-date-columns-at-run-time
df = df.apply(lambda col: pd.to_datetime(col, errors = 'ignore')
              if col.dtypes == object
              else col,
              axis = 0)

#replace accents
##http://stackoverflow.com/questions/37926248/how-to-remove-accents-from-values-in-columns

cols = df.select_dtypes(include = [np.object]).columns
df[cols] = df[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))


#####
#replace blank values  
#####
df.replace(r'\s+( +\.)|#',np.nan,regex=True).replace('',np.nan)

"""""
http://stackoverflow.com/questions/30392720/pandas-dataframe-replace-blanks-with-nan
if you want to replace Nan values by another string: df = df.fillna('string')
http://pandas.pydata.org/pandas-docs/stable/missing_data.html
"""""
#
#print df.columns
#print(df.dtypes)
#print (df.shape)
#print (df.head(0))	


replace_y = [r"\boui\b", r"\by\b", r"\byes\b"]
replace_n = [r"\bnon\b", r"\bn\b", r"\bno\b"]


""""
Generate descriptives data and write them in an excel file
"""""
row = 0 #row to start writing the tabs in the excel file

for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == np.object: # Only apply for columns with categorical strings
         if len(df[feature].unique()) <=6 : #select only objects with no more than 6 different values to avoid 'comments' columns
               df[feature] = df[feature].str.lower()
               print (feature, df[feature].unique()) #print before transformation
               df[feature] = df[feature].replace(replace_n, 0, regex=True)
               df[feature] = df[feature].replace(replace_y, 1, regex=True)
               #check if replace worked !
               if all(x in df[feature].unique() for x in [0,1]) == True:
                   print ('success: ', feature, df[feature].unique()) #print after transformation if applicable
                
#               generate tables with statistics 
               tab = pd.crosstab(index = df[feature], columns = "count")
#               convert in percents
#               tab = (tab/tab.sum())*100
               tab.to_excel(writer_descriptive, sheet_name = 'tabs', startrow = row)
#               translate tables downards                          
               if len(target_list) >0 :
                   for target in target_list:
                   		if df[target].name is not df[feature].name: #don't include the chosen group columns, otherwise it throws an error
						   #write raw numbers
						   tab = pd.crosstab(index = df[feature], columns = df[target], margins=True)
						   tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = 3, startrow = row)
						   #write in percent
						   tab = pd.crosstab(index = df[feature], columns = df[target], normalize = 'all', margins=True)
						   tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = len(df[target].unique()) + 6, startrow = row)
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
               tab.to_excel(writer_descriptive, sheet_name = 'tabs', startrow = row)
                          
               if len(target_list) > 0:
                   for t in target_list:
                       if df[t].name is not df[feature].name: #don't include the chosen group columns, otherwise it throws an error
                           #write raw numbers
                           tab = pd.crosstab(index = df[feature], columns = df[t], margins=True)
                           tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = 3, startrow = row)
                           #write in percent
                           tab = pd.crosstab(index = df[feature], columns = df[t], normalize = 'all', margins=True)
                           tab.to_excel(writer_descriptive, sheet_name = 'tabs', startcol = len(df[t].unique()) + 6, startrow = row)
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
                           #there is 8 datas displayed each time, so translate down 8*number of unique target values
                           row = row + len(df[t].unique())*8 + 5
               else:
                   row = row  + 2



"""""
Create graph visualization 
"""""

#binary var
pd.options.display.mpl_style = 'default'

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
                            df.boxplot(column = feature, by = df[t], grid=True, return_type=None)
                            plt.savefig(folder_path+'/graph/'+feature+'_'+t+'_boxplot.png', bbox_inches='tight')
#                            plt.show()

                            df.hist(column = feature, by = df[t], grid=True)
                            plt.suptitle(feature)
                            plt.savefig(folder_path+'/graph/'+feature+'_'+t+'_hist.png', bbox_inches='tight')
                            plt.show()


#Summary of description af all continuous variables
describe = df.describe(include='all')
#write in csv
#describe.to_csv(folder_path+'/descriptif.csv', encoding = 'utf8')       
#write excel

describe.to_excel(writer_descriptive, sheet_name = 'descriptif')

#add missing values count
worksheet_descriptif = writer_descriptive.sheets['descriptif']

#define titles of each row
bold_title = workbook_descriptive.add_format({'bold': True}) #define bold style for all column titles

##a.raw number of missing values
worksheet_descriptif.write_string(13,0,"count of missing values", bold_title)
##b.percent of missing values
cell_format_percent = workbook_descriptive.add_format({'num_format': '0.00%'})
worksheet_descriptif.set_row(14, None, cell_format_percent)#set row in percent
worksheet_descriptif.write_string(14,0,"% of missing values", bold_title)

worksheet_descriptif.write_string(17,0,"All calculations are made without taking care of missing values!!!")


i=1
for col in df.columns:
    worksheet_descriptif.write_number(13,i,df[col].isnull().sum()) #number of missing values
    worksheet_descriptif.write_number(14,i, float(df[col].isnull().sum())/len(df[col]))  #% of missing values
    i+=1

#####Create a dictionnary of each column
worksheet_descriptive = workbook_descriptive.add_worksheet('dic') #create the "dic" sheet
worksheet_descriptive.write_string(0,0,"column name")
worksheet_descriptive.write_string(0,1,"data type")
worksheet_descriptive.write_string(0,2,"definition")

i = 1
for col in df.columns:
    worksheet_descriptive.write_string(i,0,col)
    worksheet_descriptive.write_string(i,1,str(df[col].dtype))
    i+=1

#####set properties for first row and first column
#http://stackoverflow.com/questions/34757703/how-to-get-the-longest-length-string-integer-float-from-a-pandas-column-when-the/34757855#34757855

for i, j in enumerate (df.columns):
    #1/ get the max length of the describe series
    field_length = describe[j].astype(str).map(len)
    max_length = describe.loc[field_length.argmax(), j]   
    #combine title len and max length of the series, get the highest value to define the column width
    max_larg = [len(str(max_length)), len(j)]
    
    worksheet_descriptif.set_column(i+1,i+1, max(max_larg), None)
    
    #####2/Row titles
    worksheet_descriptif.set_column(0,0, 20, bold_title)
    
#save descriptive file
writer_descriptive.save()


#####
#####Create a file with all "cleaned" data
#####

#export newly created df in a csv and/or xls file according to anyone for later analysis
if 'index' not in df:
    df = df.reset_index()
#if os.path.isfile(folder_path+'/'+excel+'.csv') == False: ###if you don't want to replace csv file
df.to_csv(folder_path+'/data/'+excel_name+'.csv', index=False, encoding = 'utf8')      

#if os.path.isfile(folder_path+'/'+excel+'.xlsx') == False: ###if you don't want to replace xls file
writer_df = pd.ExcelWriter(folder_path+'/data/'+excel_name+'.xlsx', engine = 'xlsxwriter')
df.to_excel(writer_df, sheet_name = 'data')
writer_df.save()



