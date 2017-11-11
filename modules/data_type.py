#!/usr/bin/python
# -*- coding: utf-8 -*-

"""""
Useful links

https://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/

We assume that all the data are in one sheet in a single excel file. You can parse and modify this script
to gather or create multiple sheets...


"""""

from save_datas import * #to save descriptive datas into an excel file
from clean_file import * #clean df...->binary, columns title...
from dataframe_analyse import * #analyze type of each column


####
#Define actions to perform for each type of data serie (binary, categorial, continuous)
class dataType:
    
    #args: writer to write in excel and row to start the table
    def __init__(self, name, serie, *args): 
        self.name = name
        self.serie = serie
        
    def binary(self):
        graph(self.serie).histogram_cat(self.name)
        save_data(self.name, self.serie, writer).count_values()
         
    def categorical(self):
        graph(self.serie).histogram_cat(self.name)
        save_data(self.name, self.serie, writer).count_values()
    
    def continuous(self):
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
    
    def __init__(self, name, serie, group):
        self.name = name
        self.serie = serie
        self.group = group
    
    def binary (self):
        #generate bar graph
        
        graph(self.serie).histogram_cat_grouped(self.name, self.group)
        #save datas in excel file
        save_data(self.name, self.serie, writer).count_values_groupes(self.group, data) 

    def categorical(self):
        #generate bar graph
        graph(self.serie).histogram_cat_grouped(self.name, self.group)
        #save datas in excel file
        save_data(self.name, self.serie, writer).count_values_groupes(self.group, data) 

    def continuous(self):
        #generate graphs: histo and box plot
        graph(self.serie).boxplot_grouped(self.name, self.group)
        graph(self.serie).histogram_continuous_grouped(self.name, self.group)
        #save datas in excel file
        save_data(self.name, self.serie, writer).continuous_values_groupes(self.group, data)
        
        
    def objec(self):
        pass
    
    def single(self):
        pass
       
class save_data:
     #args if for writer and row
     #if not passed as args, it has to be added to to the datatype class
     #which will overload the arguments !!!
    def __init__(self, name, serie, *args):
        self.name = name
        self.serie = serie
        self.writer = writer
        self.workbook = writer.book
    
        #define style
        self.bold = workbook.add_format({'bold': True}) #define bold style for all column titles
        self.percent = workbook.add_format({'num_format': '0.00%'})
    
#    @fn_timer
    def row_col (self, func, unique_groups = 0 ): #args if for group 
        global row, row_grouped, col
        
        if func == 'count_values':
            row = row + self.serie.nunique() + 5
        if func == 'count_values_groupes':
            row = row_grouped = row_grouped + (self.serie.nunique() * unique_groups) + 3 #multiplication is for each categorie time number of unique values
        if func == 'continuous_values_groupes':
           n = 6
           row = row_grouped = row + n
        
        
#    @fn_timer    
    def count_values(self):
        global row # define row as a global variable to allow it to be modified inside the function and used outside the function
        
        #generate tables with statistics 
        tab_count = pd.crosstab(index = self.serie, columns = "count",  margins=True, )#margins_name='count') 
        tab_percent = pd.crosstab(index = self.serie, columns = 'percent', normalize = 'columns', margins=False)
    
        tab = (pd.concat([tab_count, tab_percent], axis=1))
        tab.to_excel(self.writer, sheet_name = 'tables', startrow = row) 

        #convert in percents
#        tab = (tab/tab.sum())*100
#        tab = pd.crosstab(index = self.serie, columns = '%', normalize = 'columns', margins=False)
#        tab.to_excel(self.writer, startcol = 3, sheet_name = 'tabs', startrow = self.row)
        save_data(self.name, self.serie).row_col('count_values')
                                           
    def count_values_groupes(self, group, data):
       global row, row_grouped # define row as a global variable to allow it to be modified inside the function and used outside the function
       #if the column is the choosen group, then it won't be analyzed in the grouped analysis, then down rows
       if group.name == self.name:
           row_grouped = row
       
        #write raw numbers
       """""tab = pd.crosstab(index = self.serie, values = self.serie, columns = group, margins=True)
       tab.to_excel(writer, sheet_name = 'tabs', startcol = 3, startrow = row)
       #write in percent
       tab = pd.crosstab(index = self.serie, columns = group, normalize = 'all', margins=True)
       tab.to_excel(writer, sheet_name = 'tabs', startcol = len(group.unique()) + 6, startrow = row)
       #translate tables downards
       
       global row # define row as a global variable to allow it to be modified inside the function and used outside the function
       row = row + self.serie.nunique() + 3
    """""
       if group.name is not self.name: #don't include the chosen group columns, otherwise it throws an error
           def percConvert(ser):
#               return ser/float(ser[-1])
               return ser*100
           
           tab_count = pd.crosstab(index = [self.serie,group], columns='count')
           tab_percent = pd.crosstab(index = [self.serie,group], columns = 'percent', normalize = 'columns', margins=False).apply(percConvert, axis=1)
#           test = pd.crosstab(index = [self.serie,group], columns='count').apply(lambda r:"{:.2f}".format((r/len(self.serie)*100))+'%',axis = 1)
           table_indiv = pd.crosstab(index = [self.serie], columns=group)

           #table_indiv.to_excel(self.writer, sheet_name = 'tables', startrow = row_grouped+1, startcol= 5)   

           tab = (pd.concat([tab_count, tab_percent], axis=1))
           tab.to_excel(self.writer, sheet_name = 'tables', startrow = row_grouped, startcol = 5)   
           
           unique_groups = len(group.unique()) #number of unique values in the group column
           save_data(self.name, self.serie).row_col('count_values_groupes', unique_groups)

           
    def continuous_values_groupes(self, group, data):
        global row, row_grouped 
            
        if group.name is not self.name: #don't include the chosen group columns, otherwise it throws an error
           
           #create a table grouped_by with descriptive values 
           table = self.serie.groupby(group).describe()
           
           #write title of the column analyzed
           worksheet_table_name = self.writer.sheets['tables']
           worksheet_table_name.write_string(row,0,name, self.bold)
           
           #then descends row of 1 lines and write excel
           table.to_excel(self.writer, sheet_name = 'tables', startrow = row+1)   

           save_data(self.name, self.serie).row_col('continuous_values_groupes')


