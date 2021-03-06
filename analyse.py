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

#txt processing/remove accents and cleaning file
import unicodedata

from modules.graphics import * #create graphics
from modules.save_datas import * #to save descriptive datas into an excel file
from modules.clean_file import * #clean df...->binary, columns title...
from modules.dataframe_analyse import * #analyze type of each column


#to do
#write descriptive of all columns in a separate tab->or for each column/data: create a border with all necessary informations ()

#check for missing values in 'tables' tab

#try / except for script => throw an error message !

#def to create a full description of the df: number of columns, type of columns, number of lines, 
##title of lines
##datetime of processing

####
#Define actions to perform for each type of data serie (binary, categorial, continuous)
class dataType:
    
    #args: writer to write in excel and row to start the table
    def __init__(self, name, serie, *args, **kwargs): 
        self.name = name
        self.serie = serie
        self.writer = args[0]
        self.options = options #options for graphs, analyses....
        
    def binary(self):
        if self.options['graph']:
            graph(self.serie).histogram_cat(self.name)
        save_data(self.name, self.serie, self.writer).count_values()
         
    def categorical(self):
        if self.options['graph']:
            graph(self.serie).histogram_cat(self.name)
        save_data(self.name, self.serie, self.writer).count_values()
    
    def continuous(self):
        if self.options['graph']:
            graph(self.serie).boxplot(self.name)
            graph(self.serie).histogram_continuous(self.name)
        pass
        
    def objec(self):
        pass
    
    def single(self):
        pass

####
#Define actions to perform for each type of data serie (binary, categorial, continuous)
class dataType_group:
    
    def __init__(self, name, serie, group, *args, **kwargs):
        self.name = name
        self.serie = serie
        self.group = group
        self.writer = args[0]
        self.data = args[1]
        self.options = options #options for graphs, analyses....
        
    
    def binary (self):
        #generate bar graph
        
        if self.options['graph']:
            graph(self.serie).histogram_cat_grouped(self.name, self.group)
        #save datas in excel file
        save_data(self.name, self.serie, self.writer, self.data).count_values_groupes(self.group) 

    def categorical(self):
        #generate bar graph
        if self.options['graph']:
            graph(self.serie).histogram_cat_grouped(self.name, self.group)
        #save datas in excel file
        save_data(self.name, self.serie, self.writer, self.data).count_values_groupes(self.group) 

    def continuous(self):
        if self.options['graph']:
            #generate graphs: histo and box plot
            graph(self.serie).boxplot_grouped(self.name, self.group)
            graph(self.serie).histogram_continuous_grouped(self.name, self.group)
        #save datas in excel file
        save_data(self.name, self.serie, self.writer, self.data).continuous_values_groupes(self.group)
        
        
    def objec(self):
        pass
    
    def single(self):
        pass

#create folder for each column and store all graphics
class create_folders(object):
    def __init__(self, column_name):
        self.column_name = column_name
    
    def graph(name):
        if not os.path.exists('graph'):
            os.mkdir('graph')
        if not os.path.exists('graph/'+name):
            os.mkdir('graph/'+name)
        return str('graph/'+name)
       
               
data=pd.read_excel("justine.xls", encoding = 'utf8') #sometimes some people would prefer encoding in 'cp1252'
group_columns = []
group_columns = [clean_name(name) for name in group_columns]   
               
data = cleanFile(data).column_names() #clean all column names
data = cleanFile(data).replace_binary() #replace yes/no values by 1/0
#list = cleanFile(list).column_data()

#####generate dict with type of data for each column
datatype_dict = analyseDataFrame(data).data_type()


#######################
#open excel writing
#######################
#create sheets for each topic ! 
writer = pd.ExcelWriter('descriptif.xlsx', #folder_path+'/descriptif.xlsx', 
               engine = 'xlsxwriter', 
               #default_date_format = 'dd/mm/yyyy', #change date format according to your preferences
               ) 
workbook = writer.book
worksheet_tables = workbook.add_worksheet('tables') #create tab for all descriptive tables
#https://stackoverflow.com/questions/32957441/putting-many-python-pandas-dataframes-to-one-excel-worksheet
writer.sheets['tables'] = worksheet_tables
worksheet_tables = writer.sheets['tables']
#########################


#########################

#####parse all columns of the dataframe, for each serie, apply pré defined treatment (dataType.method())

options = {
        'graph': False,
        }

for name in data.columns:
    
    #run analyses/graph associated with each column
    method = datatype_dict[name] #method contains all treatment to do for each type of data
    func = getattr(dataType(name, data[name], writer, options), method)
    func()
    
    #if there is selected groups, analyze the column for each group
    if len(group_columns)>0:
        for group in group_columns:
            func = getattr(dataType_group(name, data[name], data[group], writer, data, options), method)
            func()

#########################        

#add missing values count
#worksheet_descriptif = writer.sheets['descriptif']
#Summary of description af all continuous variables
describe = data.describe(include='all')

descriptive_missing = []
missing_raw = {}
missing_percent = {}
for col in data.columns:
    missing_raw[col] = (data[col].isnull().sum()) #number of missing values
    missing_percent[col] = (float(data[col].isnull().sum())/len(data[col]))  #% of missing values


test = pd.DataFrame([missing_raw, missing_percent], columns = data.columns, index = ['missing values', '% missing values'])
#worksheet_descriptif.write_string(20,0,"All calculations are made without taking care of missing values!!!")
describe = pd.concat([describe, test])
#print (describe)
      
#write excel
describe.to_excel(writer, sheet_name = 'descriptif')
    
    #####2/Row titles
    #define titles of each row
#    bold_title = writer.add_format({'bold': True}) #define bold style for all column titles
#    worksheet_tables.set_column(0,0, 20, bold_title)  



#set width of each column
for worksheet in workbook.worksheets():
    ExcelFormatting(worksheet, writer).column_width()


#save descriptive file=>at the very end !!!
writer.save()
 
    
""""




#define titles of each row
bold_title = workbook_descriptive.add_format({'bold': True}) #define bold style for all column titles

##a.raw number of missing values
worksheet_descriptif.write_string(17,0,"count of missing values", bold_title)



##b.percent of missing values
i=1
for col in data.columns:
    worksheet_descriptif.write_number(17,i,data[col].isnull().sum()) #number of missing values
    worksheet_descriptif.write_number(18,i, float(data[col].isnull().sum())/len(data[col]))  #% of missing values
    i+=1

cell_format_percent = workbook_descriptive.add_format({'num_format': '0.00%'})
worksheet_descriptif.set_row(18, None, cell_format_percent)#set row in percent
worksheet_descriptif.write_string(18,0,"% of missing values", bold_title)

worksheet_descriptif.write_string(20,0,"All calculations are made without taking care of missing values!!!")



#####Create a dictionnary of each column
worksheet_descriptive = workbook_descriptive.add_worksheet('dic') #create the "dic" sheet
worksheet_descriptive.write_string(0,0,"column name")
worksheet_descriptive.write_string(0,1,"data type")
worksheet_descriptive.write_string(0,2,"definition")

i = 1
for col in data.columns:
    worksheet_descriptive.write_string(i,0,col)
    worksheet_descriptive.write_string(i,1,str(data[col].dtype))
    i+=1

#####set properties for first row and first column
#http://stackoverflow.com/questions/34757703/how-to-get-the-longest-length-string-integer-float-from-a-pandas-column-when-the/34757855#34757855

for i, j in enumerate (data.columns):
    #1/ get the max length of the describe series
    field_length = describe[j].astype(str).map(len)
    max_length = describe.loc[field_length.argmax(), j]   
    #combine title len and max length of the series, get the highest value to define the column width
    max_larg = [len(str(max_length)), len(j)]
    
    worksheet_descriptif.set_column(i+1,i+1, max(max_larg), None)
    
    #####2/Row titles
    worksheet_descriptif.set_column(0,0, 20, bold_title)
    
#save descriptive file
writer.save()


#####
#####Create a file with all "cleaned" data
#####
"""""
"""""
#export newly created df in a csv and/or xls file according to anyone for later analysis
if 'index' not in data:
    df = data.reset_index()
#if os.path.isfile(folder_path+'/'+excel+'.csv') == False: ###if you don't want to replace csv file
#data.to_csv(folder_path+'/data/'+excel_name+'.csv', index=False, encoding = 'utf8')      
data.to_csv('fichier.csv', index=False, encoding = 'utf8')      

#if os.path.isfile(folder_path+'/'+excel+'.xlsx') == False: ###if you don't want to replace xls file
writer_df = pd.ExcelWriter(folder_path+'/data/'+excel_name+'.xlsx', engine = 'xlsxwriter')
df.to_excel(writer_df, sheet_name = 'data')
writer_df.save()

#####
"""""

"""""
#http://stackoverflow.com/questions/30392720/pandas-dataframe-replace-blanks-with-nan
#if you want to replace Nan values by another string: df = df.fillna('string')
#http://pandas.pydata.org/pandas-docs/stable/missing_data.html
"""""


