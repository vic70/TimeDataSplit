"""
Last Modified 2023-4-20

@author: Victor
"""

import numpy as np
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
import yaml

# Create GUI to get file
def getfile(title= "Select file",filetypes = [(("all files","*.*"))], existpath='', batchProcess = False, batchFileType='.dat'):
   root = tk.Tk()
   if not batchProcess:
      if existpath == '':
         root.title("Select Split File")
         filepath = filedialog.askopenfilename(initialdir = "__FILE__" ,title = title, filetypes = filetypes)
      else:
         filepath = existpath
      filelocation =  os.path.split(filepath)[0]
      filename =  os.path.split(filepath)[1]
      root.destroy()
      return filepath, filelocation, filename  
   else:
      root.title("Select Folder")
      folderpath = filedialog.askdirectory(initialdir = "__FILE__" ,title = title)
      # Get list of files with selected suffix in the selected folder
      file_list = []
      for dirpath, dirnames, filenames in os.walk(folderpath):
         for filename in filenames:
               if filename.endswith(batchFileType):
                  file_list.append(os.path.join(dirpath, filename))
      root.destroy()
      return folderpath, file_list
   

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

   filepath, filelocation, filename = getfile()
   
   #r'C:/Reports/2021-5-31 Infinite Next/20230327 Lotu12Max multihead BA/Data/Post Pick_No sync pick.dat')

   #file path split
   df=pd.read_table(filepath, low_memory=False)

   # Assign values to variables
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


   batchProcess = False
   if 'batchProcess' in configData['batch']:
      batchProcess = configData['batch']['batchProcess']
      batchFileType = configData['batch']['batchFileType']

   if requireConversion:
      df[newChannelName] = modifyData(df, conversionChannel, formula, two_complement)

   switchtimes= split_intervals(df, channelmode, splitmode, conditionalChannel, conditionValue, splitAtEnd, conditionExist)
   finalTable = mergeTable(df, switchtimes, ahead, behind, plotlist)

   #export final table to the filelocation in csv format, replace existing file
   finalTable.to_csv(filelocation+'\\'+filename[:-4]+'_split.csv', index=False)

if __name__ == '__main__':
    main()