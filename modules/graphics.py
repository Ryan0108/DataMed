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

from .timer import *
from .folder_tree import *

class create_folders(object):
    def __init__(self, column_name):
        self.column_name = column_name
    
    def graph_folder(name):
        if not os.path.exists('graph'):
            os.mkdir('graph')
        if not os.path.exists('graph/'+name):
            os.mkdir('graph/'+name)
        return str('graph/'+name)
       

@time_all_class_methods                 
class graph:
    def __init__(self, serie):

#        self.min = min.df
#        self.max = max.df
        self.serie = serie
        plt.style.use('default')
    
    def histogram_continuous(self, name):
        serie = self.serie
        ax = serie.plot.hist(grid=True,normed=True)
        ax.set_xlabel(name)
#        plt.savefig(folder_path+'/graph/'+feature+'_hist.png', bbox_inches='tight')
        
        #plt.show()
        folder = create_folders.graph_folder(name)
        plt.savefig(folder+'/'+name+'_'+'histogram.png', bbox_inches='tight')
        plt.close('all')
    
    def histogram_cat(self, name):
        fig, ax = plt.subplots()
#        width = 0.35
        x = np.arange((self.serie.nunique())) #get count of categories
        s = self.serie.value_counts() #create a panda df with count of each value of the categorie
        
        plt.bar(x, s.values)
        fig.suptitle(name)
        plt.xticks(x, s.index)
            
        #plt.show()
        folder = create_folders.graph_folder(name)
        plt.savefig(folder+'/'+name+'_bar.png', bbox_inches='tight')
        plt.close('all')
    
#    @fn_timer
    def histogram_continuous_grouped(self, name, group):
        serie = self.serie
        group_count = group.nunique() #set numbers of hist to display
        
        #group values by the group column
        grouped = serie.groupby(group)
        
        fig, axs = plt.subplots(nrows = 1, ncols = group_count, sharey=True, sharex= True)
        num_bins = round(len(serie)/5) #bins is 20% of all values for more granularity 
        
        #set title
        fig.suptitle(name + ' by ' + group.name, fontsize=14)
        
        #iterate through group to create pool data and display histogram
        i=0
        for key, value in grouped:
            data = np.asarray((value.dropna().tolist())) #convert to np.array and drop missing values
            axs[i].hist(data, bins = num_bins, normed=1)
            axs[i].set_title(key)
            i +=1
                    
        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        
        #        plt.savefig(folder_path+'/graph/'+feature+'_hist.png', bbox_inches='tight')

        #plt.show()
        folder = create_folders.graph_folder(name)
        plt.savefig(folder+'/'+name+'_'+group.name+'_histogram.png', bbox_inches='tight')
        plt.close('all')

    def histogram_cat_grouped(self, name, group):
        
        #setting the positions and width for the bars
        width = 0.35
        position = np.arange ((group.nunique())) #get count of groups
        
        categories = self.serie.dropna().unique()
        
        #plotting the bars
#        fig, ax = plt.subplots()
        
        #####arrange data        
        #group values of categories by group, and count each unique value
        grouped = group.groupby(self.serie)
        
        d ={} #create a dict to create a new dataframe with index for category and title for the group
        for key, serie in grouped: #name is the group, and group the serie with title as the category
            d[key] = serie.value_counts()

        df = pd.DataFrame(d)

        #for each group, create bars equal to the count of values for each categorie
        #in position: 'position'        

        ax = df.plot(kind='bar', 
                     grid = True,
                     title = ('bar: ' + name +', grouped by ' + group.name) ,
                     sort_columns = True,
                     )
        
#        i=0
#        for name in df.columns:
#            print (df[name])
#            plt.bar(position, 
#                    #using first group data
#                    df[name],
#                    #of width
#                    width*i,
#                    #with alpha 0.5
#                    alpha=0.5,
#                    #with color
#                    color = "#EE3224",
#                    #with label the first group
#                    label = name)

#        plt.show()
        folder = create_folders.graph_folder(name)
        plt.savefig(folder+'/'+name+'_'+group.name+'_bar.png', bbox_inches='tight')
        plt.close('all')
    
#    @fn_timer
    def boxplot(self, name):
        serie = self.serie
        fig, ax = plt.subplots()
        fig.suptitle(name)
        data = np.asarray((serie.dropna().tolist())) #convert to np.array and drop missing values
        ax.boxplot(data, 
                   labels= ['serie'],
                   notch=False)
        
        
        #plt.show()
        folder = create_folders.graph_folder(name)
        plt.savefig(folder+'/'+name+'_boxplot.png', bbox_inches='tight')
        plt.close('all')
    
#    @fn_timer
    def boxplot_grouped(self, name, group):
        #http://matplotlib.org/examples/pylab_examples/boxplot_demo2.html
        #http://matplotlib.org/examples/pylab_examples/boxplot_demo.html
        #http://matplotlib.org/api/axes_api.html?highlight=boxplot#matplotlib.axes.Axes.boxplot
        
        serie = self.serie
        fig, ax = plt.subplots()
       
        #####arrange data        
        #group values of categories by group, and count each unique value
        grouped = serie.groupby(group)

        data = [] #list of list of data
        label = [] #list of name of each group
        for key, serie in grouped: #key is the group, and serie the serie with title as the category
            dataset = (serie.dropna().tolist())
            label.append(key)
            data.append(dataset) 

        pos = np.array(range(len(data))) + 1
        
        plt.boxplot(data, 
                    notch=False, 
                    showmeans= True,
                    labels = label)
        
        plt.suptitle(name + ' by ' + group.name)
#        xtickNames = plt.setp(ax, xticklabels=group.dropna().unique())
#        plt.setp(xtickNames, rotation=45, fontsize=8)
        
        fig.text(0.2,0.02,'orange bar: median, green triangle: mean')
        
#        plt.show()
        folder = create_folders.graph_folder(name)
        plt.savefig(folder+'/'+name+'_'+group.name+'_boxplot.png', bbox_inches='tight')
        plt.close('all')

