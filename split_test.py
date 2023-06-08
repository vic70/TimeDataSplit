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
import CommonUtil
#import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import plotly.express as px
import plotly.graph_objects as go
import yaml
from plotly.subplots import make_subplots
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

#function to read the below parameters from a file in yml format
def readyml():
   filepath, filelocation, filename = getfile(title= "Select yml config",filetypes = [(("yaml file","*.yml"))])
   with open(filepath, 'r') as file:
      configData = yaml.safe_load(file)
   return configData


#merge different segments into same table
def mergeTable(df, switchtimes, ahead, behind, plotlist):
   tableMerge = pd.DataFrame()
   sampleRate = 8 # in kHz
   tableMerge['Time (ms)'] =  np.arange(0, ahead+behind, sampleRate)

   for t in switchtimes:
      if t > ahead*sampleRate and t< (df.shape[0] - behind*sampleRate):  #trigger not at begining and ending
         df.loc[int(t-ahead*sampleRate):int(t+behind*sampleRate),'Channel_Switch'] = np.array(True)
         tableSlice=df.iloc[int(t-ahead*sampleRate):int(t+behind*sampleRate)][plotlist].add_suffix('_t='+str(t)).reset_index(drop=True)
         tableMerge=pd.concat([tableMerge,tableSlice], axis=1)
   return tableMerge

# find the interval to be split

def split_intervals(df, channelmode, splitmode, conditionalChannel='', conditionValue='', splitAtEnd=True,
                    conditionExist=False):
    # splitAtEnd get the time when the channel switch from splitmode to other mode
    if splitAtEnd:
        df['Channel_Switch'] = np.logical_and((df[channelmode].shift(-1) != df[channelmode]),
                                              df[channelmode] == splitmode)
    # splitAtEnd get the time when the channel switch from other modes to split mode
    else:
        df['Channel_Switch'] = np.logical_and((df[channelmode].shift(-1) != df[channelmode]),
                                              df[channelmode].shift(-1) == splitmode)
        # add condition to the split
    if conditionExist:
        df['Channel_Switch'] = np.logical_and(df['Channel_Switch'], eval('df[conditionalChannel]' + conditionValue))

    switchtimes = np.array(df.loc[df['Channel_Switch']]['sample'])


    return switchtimes     # this is in sample unit


def create_scatter(fig, x, y, row, col):
   fig.add_trace(go.Scatter(x=x, y=y, mode="lines", line=dict(dash='solid')),
                 row=row,
                 col=col
                 )
   return fig

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

   plotlist = configData['plotChannel']['plotlist']

   multiFileSupport = configData['multiFileSupport']['Input']

   requireFunc = configData['function']['requireFunc']
   applyChName = configData['function']['applyChName']
   newChName = configData['function']['newChName']
   funcs = [getattr(CommonUtil, i) for i in configData['function']['funcs']]
   funcsInputs = configData['function']['funcsInput']

   filepath, filelocation, filename = getfile(multiFileSupport)

   if multiFileOutput:
      for i in range(len(filepath)):
         df=pd.read_table(filepath[i], low_memory=False)

         if requireFunc:
            for j in range(len(funcs)):
               if not funcsInputs[j]:
                  df[newChName[j]] = funcs[j](df[applyChName[j]])
               else:
                  df[newChName[j]] = funcs[j](df[applyChName[j]], funcsInputs[j])

         switchtimes= split_intervals(df, channelmode, splitmode, conditionalChannel, conditionValue, splitAtEnd, conditionExist)

         finalTable = mergeTable(df, switchtimes, ahead, behind, plotlist)
         finalTable.to_csv(filelocation[i]+'\\'+filename[i][:-4]+'_split.csv', index=False)
   else:
      for i in range(len(filepath)):
         df = pd.read_table(filepath[i], low_memory=False)

         if requireFunc:
            for j in range(len(funcs)):
               if not funcsInputs[j]:
                  df[newChName[j]] = funcs[j](df[applyChName[j]])
               else:
                  df[newChName[j]] = funcs[j](df[applyChName[j]], funcsInputs[j])

         switchtimes = split_intervals(df, channelmode, splitmode, conditionalChannel, conditionValue, splitAtEnd,
                                       conditionExist)
         finalTable = mergeTable(df, switchtimes, ahead, behind, plotlist)

         # k2 = plotlist[0]
         # k = df[plotlist[0]]
         tgt = df[df['Channel_Switch'] == True]
         time = np.arange(tgt.shape[0])



         fig = make_subplots(
            rows = 3,
            cols = 1,
         )
         create_scatter(fig, time, tgt[plotlist[3]],1,1 )
         create_scatter(fig, time, tgt[plotlist[5]],2,1 )
         create_scatter(fig, time, tgt[plotlist[7]],3, 1)
         # Create a new Figure object and add scatter plots for each channel

         fig.show()





if __name__ == '__main__':
    main()
    
    



    