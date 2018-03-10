#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

#define row start for excel writing
row = 0 #start of descriptive tables
row_grouped = 0 #start of descriptive tables for grouped data


class destinationPath (object):
    
    def __init__(self, root):
        self.root = root
    
    def folder_name(self, name):
        return (root+'/'+name) #return name of the folder                                                                 


class create_folders(object):
    def __init__(self, column_name):
        self.column_name = column_name
    
    def graph_folder(name):
        if not os.path.exists('graph'):
            os.mkdir('graph')
        if not os.path.exists('graph/'+name):
            os.mkdir('graph/'+name)
        return str('graph/'+name)