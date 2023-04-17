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
import xml.etree.ElementTree as ET



# Create GUI to get file

def getfile(title= "Select file",filetypes = [(("all files","*.*"))], existpath=''):

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
   # print(f'df.shape[0]= {df.shape[0]}')
   # print(df.iloc[5000:5050][plotlist])

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
   #print range of df['new']
   #print(f'range of df[new] = {df["new"].min()} to {df["new"].max()}')
   
   if two_complement:
      #change df['new'] to integer type
      df['new'] = df['new'].astype('int')
      df['new'] = df['new'].apply(twos_complement, args=(16,))
      #print(f'range of df[new] after if = {df["new"].min()} to {df["new"].max()}')
   
   df['new'] = eval('df.new'+formula)

   #print(f'range of df[new] after formula = {df["new"].min()} to {df["new"].max()}')

   return df.new


# #function to read the below parameters from a file in xml format 
# def readxml():
#    filepath, filelocation, filename = getfile(title= "Select XML config",filetypes = [(("xml files","*.xml"))])
#    print(filepath)
#    tree = ET.parse(filepath)
#    return tree
#    # for child in root:
#    #    print(child.tag, child.attrib)
#    #    for subchild in child:
#    #       print(subchild.tag, subchild.attrib)



def main():

   # tree = readxml()

   filepath, filelocation, filename = getfile()
   
   #r'C:/Reports/2021-5-31 Infinite Next/20230327 Lotu12Max multihead BA/Data/Post Pick_No sync pick.dat')


   #file path split

   #path_to_output = filelocation

   df=pd.read_table(filepath, low_memory=False)

   #Define condition

   #for cap sense


   #root = tree.getroot()
   #print(root.find('split setting').find('split parameters').find('channelmode').text)


#for large bond force
   #split parameters
   channelmode = 'GMP_OCA_PORT_20'
   splitmode = 2
   splitAtEnd=False

   # data collect before and after the switch
   ahead = 50  #ms
   behind = 100   #ms

   #condition parameters
   conditionExist = False
   conditionalChannel = 'CMD_POS_BHG2_Z'
   conditionValue = '<-70000'

   #conversion parameters
   requireConversion=False
   conversionChannel= 'WH_ADC_PORT_WAFERCOOLINGFLOWSNR_R'
   newChannelName = 'Cap sense (V)'
   formula = '*10/32767'
   two_complement=True

   #plot parameters
   plotlist=['ENC_POS_BHG2_Z','DAC_BHG2_Z','ENC_POS_BHG2_BF_VCM','GMP_OCA_PORT_20']


# '''
# #for cap sense
#    #split parameters
#    channelmode = 'MODE_DP_LZ'
#    splitmode = '1f010001'
#    splitAtEnd=True

#    #condition parameters
#    conditionExist = False
#    conditionalChannel = 'CMD_POS_BHG2_Z'
#    conditionValue = '<-70000'

#    #conversion parameters
#    requireConversion=True
#    conversionChannel= 'WH_ADC_PORT_WAFERCOOLINGFLOWSNR_R'
#    newChannelName = 'Cap sense (V)'
#    formula = '*10/32767'
#    two_complement=True

#    #plot parameters
#    plotlist=['MODE_DP_LY','CMD_POS_DP_LZ','ENC_POS_DP_LZ','Cap sense (V)']

# '''
   
# '''
#    For BHZ laser

#    channelmode = 'MODE_BHG2_Z'
#    splitmode = 'ff010001'
#    conditionalChannel = 'CMD_POS_BHG2_Z'
#    conditionValue = '<-70000'
#    plotlist=['CMD_POS_BHG2_Z','Laser (um)']
#    conversionChannel= 'EJ_ADC_PORT_VAC'
#    newChannelName = 'Laser (um)'
#    formula = '*0.03063'
#    splitAtEnd=True
#    conditionExist=True
  
# '''


   #print(df['EJ_ADC_PORT_VAC'].dtype)

   if requireConversion:
      df[newChannelName] = modifyData(df, conversionChannel, formula, two_complement)

   switchtimes= split_intervals(df, channelmode, splitmode, conditionalChannel, conditionValue, splitAtEnd, conditionExist)
   finalTable = mergeTable(df, switchtimes, ahead, behind, plotlist)

   #export final table to the filelocation in csv format, replace existing file
   finalTable.to_csv(filelocation+'\\'+filename[:-4]+'_split.csv', index=False)



if __name__ == '__main__':
    main()









# print(filename)
# print(os.path.split(filename)[0])
# print(os.path.split(filename)[1])



# filenames = glob.glob('*.txt')

# print(filenames)

# plotId= np.arange(len(filenames))

# print(plotId)


# time_save=8*200 #samples*ms

# path_to_output = r'C:\Reports\2019-12-8 Infinite\2020-12-1 Detect suck back fail issue\Split datalog'


# for id in plotId:
    

#     print(id)
#     filename = os.path.basename(filenames[id])
    
#     dp=pd.read_table(filenames[id],delimiter=r"\s+")
#     portlist_name = list(dp.iloc[1:1])
#        # print(list(dp.columns))
    
#  #BH_Vac=TRUNC(MOD('IO_N1_OUT_PORT_BHG2', POWER(2,9))/POWER(2,8))
#  #BH_WB=TRUNC(MOD(K2, POWER(2,10))/POWER(2,9))+3
    
#     dp['BH_Vac'] = np.trunc(dp['IO_N1_OUT_PORT_BHG2']%(2**9)/(2**8)) 
#     dp['BH_WB'] = np.trunc(dp['IO_N1_OUT_PORT_BHG2']%(2**10)/(2**9)) 
#     dp['Vac_Switch']=  dp['BH_Vac'].shift(-1)- dp['BH_Vac']


#     #Solenoid on off time in sample
#     vac_on_time = list(dp.loc[dp['Vac_Switch'] <-0.5]['Sample'])
#     vac_off_time = list(dp.loc[dp['Vac_Switch'] >0.5]['Sample'])

#     airflows = pd.DataFrame()
    
#     for i in range(len(vac_on_time)):
#        #make sure last on off have enough data
#         if(vac_on_time[i]+time_save < dp['Sample'].iloc[-1]):
#             airflows['On'+str(i)] = list(dp[dp['Sample'].between(vac_on_time[i],vac_on_time[i]+time_save)]['BHG2_ADC_PORT_AIRFLOW_MISSING_DIE'])
    
#     print(filename[:-4])
#  #   print(path_to_output + str(filename[:-4]) + '.csv')
#     airflows.to_csv(path_to_output + '\\'+ str(filename[:-4]) + '.csv')
#     #airflows.to_csv(r'../'+filename+'_airflow.csv')







#for col_on in airflows.columns: 
#    airflows[col_on].plot(ax=ax)
 
 


#Plot graph

#fig, axes = plt.subplots(nrows=3, ncols=1)
#ax2=ax1.twinx()
#dp.loc['50000':'55000','BHG2_ADC_PORT_AIRFLOW_MISSING_DIE'].plot(ax=axes[0])
#dp.loc['50000':'55000','BH_Vac'].plot(ax=axes[1])
#dp.loc['50000':'55000','Vac_Switch'].plot(ax=axes[2])


#dp.loc['50000':'55000','BH_WB'].plot(ax=axes[2])





    #print(dp['IO_N1_OUT_PORT_BHG2'].iloc[3])
    
 #  dp['BH_Vac']= bin(dp['IO_N1_OUT_PORT_BHG2'])[-9:-8]
   # dp['BH_WB']= bin(dp['IO_N1_OUT_PORT_BHG2'])[-10:-9]
   # dp.loc['BHG2_ADC_PORT_AIRFLOW_MISSING_DIE','BH_Vac'].plot()
    #ax=axes[0,0](ax=axes[1,0]
    
    



    