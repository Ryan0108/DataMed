#!/usr/bin/python
# -*- coding: utf-8 -*-

"""""
Useful links

https://www.analyticsvidhya.com/blog/2016/07/practical-guide-data-preprocessing-python-scikit-learn/

We assume that all the data are in one sheet in a single excel file. You can parse and modify this script
to gather or create multiple sheets...


"""""
import datetime
import time


#####
#timer for classes !
#####
#https://www.codementor.io/sheena/advanced-use-python-decorators-class-function-du107nxsv
def time_this(original_function):      
    def new_function(*args,**kwargs):
        before = datetime.datetime.now()  
        t0 = time.time()                   
        x = original_function(*args,**kwargs)
        t1 = time.time()                
        after = datetime.datetime.now()                      
#        print ("Elapsed Time = {0}".format(after-before) )     
#        print ("Total time running %s: %s seconds, t0 %s, t1 %s" %
#               (original_function.__qualname__, str(t1-t0), t0, t1)
#               )
        return x                                             
    return new_function  

def time_all_class_methods(Cls):
    class NewCls(object):
        def __init__(self,*args,**kwargs):
            self.oInstance = Cls(*args,**kwargs)

        def __getattribute__(self,s):
            """
            this is called whenever any attribute of a NewCls object is accessed. This function first tries to 
            get the attribute off NewCls. If it fails then it tries to fetch the attribute from self.oInstance (an
            instance of the decorated class). If it manages to fetch the attribute from self.oInstance, and 
            the attribute is an instance method then `time_this` is applied.
            """
            try:    
                x = super(NewCls,self).__getattribute__(s)
            except AttributeError:      
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(s)
            if type(x) == type(self.__init__): # it is an instance method
                return time_this(x)                 # this is equivalent of just decorating the method with time_this
            else:
                return x
    return NewCls



