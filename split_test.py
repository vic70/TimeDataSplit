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
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from dashing import DashApp, ScatterPlot

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
### deprecated


# def create_scatter_plots(df_list):
#     app = dash.Dash(__name__)

#     # Create dropdown options from DataFrame columns
#     dropdown_options = [{'label': f'{col}', 'value': col} for col in df_list.columns]

#     app.layout = html.Div([
#         dcc.Dropdown(
#             id='dropdown',
#             options=dropdown_options,
#             value=(df_list.columns[0],df_list.columns[0] ),
#             multi= True
#         ),
#         dcc.Graph(id='scatter-plot')
#     ])

#     @app.callback(
#         Output('scatter-plot', 'figure'),
#         [Input('dropdown', 'value')]
#     )
#     def update_figure(selected_cols):
        
#         if len(selected_cols) <= 1:
#          return go.Figure(data=[], layout=go.Layout(title=go.layout.Title(text="Please select at two column to plot.")))
        
#         fig = make_subplots(specs=[[{"secondary_y": True}]])
#         if len(selected_cols) > 1:
#          for idx, selected_value in enumerate(selected_cols):
#                if idx == 0:
#                   fig.add_trace(
#                      go.Scatter(
#                            x=df_list.index,
#                            y=df_list[selected_value],
#                            name=selected_value
#                      ),
#                      secondary_y=False
#                   )

#                if idx == 1:
#                   fig.add_trace(
#                      go.Scatter(
#                            x=df_list.index,
#                            y=df_list[selected_value],
#                            name=selected_value
#                      ),
#                      secondary_y=True
#                   )
#          fig.update_yaxes(title_text=f"<b>{selected_cols[0]}", secondary_y=False)
#          fig.update_yaxes(title_text=f"<b>{selected_cols[1]}", secondary_y=True)
#          fig.update_layout(title= f"Scatter Plot with {selected_cols[0]} and {selected_cols[1]} across Time (ms)")

#         return fig

#     return app


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

         tgt = df[df['Channel_Switch'] == True] # this is trimmed df with all cols
         time = np.arange(tgt.shape[0])


      app = ScatterPlot(tgt)
      dropdown = app.create_figure()
      app.run(dropdown)












if __name__ == '__main__':
    main()
    
    



    