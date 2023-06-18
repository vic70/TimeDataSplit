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
import plotly.express as px
import plotly.graph_objects as go
import yaml

from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from CommonClass import Config, FileSelector
from dashing import DashApp, ScatterPlot

def readyml(config_file):
    with open(config_file, 'r') as file:
        configData = yaml.safe_load(file)
    return configData

def file_split(filepath):          
   if len(filepath) > 1:
         filepath = filepath
         filelocation =  os.path.split(filepath)[0]
         filename =  os.path.split(filepath)[1]
         return filepath, filelocation, filename
   else:
      filepath = filepath
      filelocation =  [os.path.split(filepath[i])[0] for i in range(len(filepath))]
      filename =  [os.path.split(filepath[i])[1] for i in range(len(filepath))]
      return filepath, filelocation, filename   


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


def main():
   file_selector = FileSelector()
   file_selector.create_ui()
   config_file, data_files = file_selector.get_files()

   config = Config(readyml(config_file))
   filepath, filelocation, filename = file_split(data_files)

   if not isinstance(filepath, str):
      for i in range(len(filepath)):
         df=pd.read_table(filepath[i], low_memory=False)

         if config.requireFunc:
            for j in range(len(config.funcs)):
               if not config.funcsInputs[j]:
                  df[config.newChName[j]] = config.funcs[j](df[config.applyChName[j]])
               else:
                  df[config.newChName[j]] = config.funcs[j](df[config.applyChName[j]], config.funcsInputs[j])

         switchtimes= split_intervals(df, config.channelmode, config.splitmode, 
                                      config.conditionalChannel, config.conditionValue, config.splitAtEnd, 
                                      config.conditionExist)

         finalTable = mergeTable(df, switchtimes, config.ahead, config.behind, config.plotlist)
         finalTable.to_csv(filelocation[i]+'\\'+filename[i][:-4]+'_split.csv', index=False)
   else:
      for i in range(len(filepath)):
         df = pd.read_table(filepath, low_memory=False)

         if config.requireFunc:
            for j in range(len(config.funcs)):
               if not config.funcsInputs[j]:
                  df[config.newChName[j]] = config.funcs[j](df[config.applyChName[j]])
               else:
                  df[config.newChName[j]] = config.funcs[j](df[config.applyChName[j]], config.funcsInputs[j])

         switchtimes = split_intervals(df, config.channelmode, config.splitmode, config.conditionalChannel, 
                                       config.conditionValue, config.splitAtEnd,
                                       config.conditionExist)
         finalTable = mergeTable(df, switchtimes, config.ahead, config.behind, config.plotlist)

         tgt = df[df['Channel_Switch'] == True] # this is trimmed df with all cols

      app = ScatterPlot(tgt)
      dropdown = app.create_figure()
      app.run(dropdown)


if __name__ == '__main__':
    main()
    
    



    