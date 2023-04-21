# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 22:59:20 2021

@author: Nic
"""

import math
import numpy as np
import pandas as pd
import glob
import os
#import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
# import xml.etree.ElementTree as ET
import yaml
# Create GUI to get file

def getfile(multi = False,title= "Select file",filetypes = [(("all files","*.*"))], existpath=''):

   if multi:
      if existpath == '':
         root = tk.Tk()
         root.title("Split File")
         filepath = filedialog.askopenfilenames(initialdir = "__FILE__" ,title = title, filetypes = filetypes)
         root.destroy()
      else:
         filepath = existpath

      filelocation =  [os.path.split(filepath[i])[0] for i in range(len(filepath))]
      filename =  [os.path.split(filepath[i])[1] for i in range(len(filepath))]
      return filepath, filelocation, filename
   else:
      if existpath == '':
         root = tk.Tk()
         root.title("Split File")
         filepath = filedialog.askopenfilename(initialdir = "__FILE__" ,title = title, filetypes = filetypes)
         root.destroy()
      else:
         filepath = existpath
      filelocation =  os.path.split(filepath)[0]
      filename =  os.path.split(filepath)[1]
      return filepath, filelocation, filename

# find the interval to be split
def split_intervals(df, channelmode, splitmode, conditionalChannel='', conditionValue='', splitAtEnd=True, conditionExist=False):
   
   #splitAtEnd get the time when the channel switch from splitmode to other mode
   if splitAtEnd:
      df['Channel_Switch']= np.logical_and((df[channelmode].shift(-1) != df[channelmode]) , df[channelmode]== splitmode)
   
   #splitAtEnd get the time when the channel switch from other modes to split mode
   else:
      df['Channel_Switch']= np.logical_and((df[channelmode].shift(-1) != df[channelmode]) , df[channelmode].shift(-1)== splitmode)   
   
   #add condition to the split
   if conditionExist:
      df['Channel_Switch']= np.logical_and(df['Channel_Switch'],eval('df[conditionalChannel]'+conditionValue ) )   
   
   switchtimes = np.array(df.loc[df['Channel_Switch']]['sample'])

   return switchtimes

#merge different segments into same table
def mergeTable(df, switchtimes, ahead, behind, plotlist):
   tableMerge = pd.DataFrame()
   sample = 8000
   tableMerge['Time (ms)'] =  np.arange(0, ahead+behind, 1000/sample)

   for t in switchtimes:
      if t > ahead*sample/1000 and t< (df.shape[0] - behind*sample/1000):  #trigger not at begining and ending
         tableSlice=df.iloc[int(t-ahead*sample/1000):int(t+behind*sample/1000)][plotlist].add_suffix('_t='+str(t)).reset_index(drop=True)
         tableMerge=pd.concat([tableMerge,tableSlice], axis=1)
   return tableMerge

# convert 2 complement value in decimal to decimal with sign
def twos_complement(input_value, num_bits):
      mask = 2**(num_bits - 1)
      return -(input_value & mask) + (input_value & ~mask)

# function to modify data by adding a column by modifying the existing column with a fomula input in text
def modifyData(df, column, formula, two_complement=False):
   df['new'] = df[column]
   
   if two_complement:
      #change df['new'] to integer type
      df['new'] = df['new'].astype('int')
      df['new'] = df['new'].apply(twos_complement, args=(16,))
   df['new'] = eval('df.new'+formula)
   return df.new

#function to read the below parameters from a file in yml format 
def readyml():
   filepath, filelocation, filename = getfile(title= "Select yml config",filetypes = [(("yaml file","*.yml"))])
   with open(filepath, 'r') as file:
      configData = yaml.safe_load(file)
   return configData

def main():
   configData = readyml()

   multiFileInput = configData['multiFileSupport']['Input']
   multiFileOutput = configData['multiFileSupport']['Output']

   channelmode = configData['splitCondition']['channelmode']
   splitmode = configData['splitCondition']['splitmode']
   splitAtEnd = configData['splitCondition']['splitAtEnd']

   ahead = configData['data_range']['ahead']
   behind = configData['data_range']['behind']

   conditionExist = configData['condition']['conditionExist']
   conditionalChannel = configData['condition']['conditionalChannel']
   conditionValue = configData['condition']['conditionValue']

   requireConversion = configData['conversion']['requireConversion']
   conversionChannel = configData['conversion']['conversionChannel']
   newChannelName = configData['conversion']['newChannelName']
   formula = configData['conversion']['formula']
   two_complement = configData['conversion']['two_complement']

   plotlist = configData['plotChannel']['plotlist']
   multiFileSupport = configData['multiFileSupport']['Input']



   filepath, filelocation, filename = getfile(multiFileSupport)
   for i in range(len(filepath)):
      df=pd.read_table(filepath[i], low_memory=False)

      if requireConversion:
         df[newChannelName] = modifyData(df, conversionChannel, formula, two_complement)

      switchtimes= split_intervals(df, channelmode, splitmode, conditionalChannel, conditionValue, splitAtEnd, conditionExist)
      finalTable = mergeTable(df, switchtimes, ahead, behind, plotlist)
      finalTable.to_csv(filelocation[i]+'\\'+filename[i][:-4]+'_split.csv', index=False)

if __name__ == '__main__':
    main()
    
    



    