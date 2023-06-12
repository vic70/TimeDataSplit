# %% quick plot
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import pathlib
import pandas as pd
from IPython.display import HTML
from plotly.subplots import make_subplots
from ctypes import *

def parseFilePath(workdir=os.getcwd(), postfix='.dat', pattern='*'):
    filenames = list()
    print(workdir)
    objDir = pathlib.Path(workdir)
    print(pattern+postfix)
    filepaths = list(objDir.rglob(pattern+postfix))
    for filepath in filepaths:
        filenames.append(filepath.stem)
    # print(objDir)
    # print(objDir.rglob(pattern+postfix))
    # print(filepaths)
    return filepaths, filenames

def getHeader(filepath, sep='\t', range=''):
    df = pd.read_csv(filepath, sep)
    headers = df.columns.values.tolist()
    return headers
        
class Figure:
    def __init__(self, headers, df) -> None:
        self.headerList = headers
        self.traceList = list()
        self.df = df
        self.fig = go.Figure()
        
    def appendDataTrace(self, x, y, name, row, col, modes='lines'):
        if any(y in self.headerList for col in self.headerList):
            self.traceList.append(dict(x=self.df[x], y=self.df[y], name=name, row=row, col=col, mode=modes))
        else:
            # print(self.headerList)
            raise ValueError("Cannot find %s in header list\n%s" % (y, self.headerList))
            
    def setupPlot(self, shared_x=False, shared_y=False):
        max_row = max([trace['row'] for trace in self.traceList])
        max_col = max([trace['col'] for trace in self.traceList])
        self.fig = make_subplots(rows=max_row, cols=max_col, shared_xaxes=shared_x, shared_yaxes=shared_y)
        for trace in self.traceList:
            tt = go.Scatter(x=trace['x'],y=trace['y'], name=trace['name'], mode=trace['mode'])
            self.fig.add_trace(trace=tt, row=trace['row'], col=trace['col'])
            
    def drawPlot(self):
        self.fig.show()
        
    def updatePlotLayout(self, **kwargs):
        self.fig.update_layout(kwargs)

def hex2double(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float

def dec2hex(input, bits=64):

    if (bits == 32):
        output = hex(input & (2**32-1))
    elif (bits == 64):
        output = hex(input & (2**64-1))
    else:
        raise ValueError("Only suupport 32 and 64 bits")
    
    return output

def int2double(s):
    s_hex = dec2hex(s)
    s_double = hex2double(s_hex)
    return s_double

def castInt2Double(df, col_name):
    temp = df.pop(col_name)
    temp1 = np.array(temp, dtype=np.int32)
    temp2 = np.array([])
    
    for x in temp1:
        temp2 = np.append(temp2, (int2double(int(x))))
    
    df.insert(loc=df.shape[1], column=col_name, value=temp2.tolist())
    return df

def addTimeMsColumn(df, inputColName='sample', removeOfst=True, samplingFreq=8000, outputColName='time_ms'):
    temp = df[inputColName]
    
    if removeOfst:
        temp1 = np.array(np.arange(start=0,stop=temp.shape[0]))
    else:
        temp1 = np.array(temp)
    
    temp2 = temp1 / samplingFreq * 1000
    df.insert(loc=df.shape[1], column=outputColName, value=temp1.tolist())
    return df

def main():

    # workdir = r"C:\Reports\2019-12-8 Infinite\20230308 ALB vibration issue\TICD inf ALB\20230320 DAC mode error in autobond"
    workdir = r"C:\Reports\2019-12-8 Infinite\20230308 ALB vibration issue\DA1075 ALB shake 20230418\datalog"
    #r'\\10.103.102.133\AD8312_Series\Meeting\20230208_iTouch2 false trigger in 19F machine'
    filepaths, filenames = parseFilePath(workdir=workdir,postfix='.txt')
    print(len(filepaths))

    fileno = 0          #select first file
    print(filepaths[fileno])
    df = pd.read_csv(filepaths[fileno], sep='\t')
    # df = df.tail(20000)
    headers = df.columns.values.tolist()
    
    print(headers)
    
    fig1 = Figure(headers, df)
    
    fig1.appendDataTrace('Sample',   'BHG2_YU_CMDPOS_PORT', 'CmdPos_Y', 1, 1)
    fig1.appendDataTrace('Sample',  'BHG2_YU_ENC_PORT_0', 'EncPos_Y', 1, 1)
    fig1.appendDataTrace('Sample',  'BHG2_YU_DAC_PORT', 'DAC_Y', 2, 1)
    fig1.appendDataTrace('Sample',  'BHG2_ALB_CMDPOS_PORT', 'CmdPos_ALB', 3, 1)
    fig1.appendDataTrace('Sample',  'BHG2_ALB_DAC_PORT', 'DAC_ALB', 4, 1)
    # fig1.appendDataTrace('sample', 'GMP_OCA_PORT_11', 'Enable Cntr', 3, 1)
    # fig1.appendDataTrace('sample', 'ENC_POS_BHG2_BF_VCM', 'Disable Cntr', 4, 1)
    # fig1.appendDataTrace('sample', 'DAC_BHG2_BF_VCM', 'Disable Cntr', 4, 1)
    # fig1.appendDataTrace('sample', 'GMP_OCA_PORT_10', 'Reset Cntr', 5, 1)
    
    # fig1.appendDataTrace('sample', 'CMD_POS_BHG2_Z', 'CmdPos_Z', 1, 1)
    # fig1.appendDataTrace('sample', 'ENC_POS_BHG2_Z', 'EncPos_Z', 1, 1)
    # fig1.appendDataTrace('sample', 'GMP_OCA_PORT_24', 'CmdPos_ALB', 1, 1)
    # fig1.appendDataTrace('sample', 'DAC_BHG2_Z', 'DAC_ALB', 2, 1)
    # fig1.appendDataTrace('sample', 'GMP_OCA_PORT_11', 'Enable Cntr', 3, 1)
    # fig1.appendDataTrace('sample', 'ENC_POS_BHG2_BF_VCM', 'Disable Cntr', 4, 1)
    # fig1.appendDataTrace('sample', 'DAC_BHG2_BF_VCM', 'Disable Cntr', 4, 1)
    # fig1.appendDataTrace('sample', 'GMP_OCA_PORT_10', 'Reset Cntr', 5, 1)

    fig1.setupPlot(shared_x=True)
    fig1.updatePlotLayout(height=1200, width=800)
    fig1.drawPlot()
    
        
    
   
    # trace_list.append(dict(x=df['sample'], y=df['ENC_POS_BHG2_ALB'], name='EncPos_ALB'))
    
    # sample = df['sample']
    # sample = sample - sample.iloc[0]
    # cmdyu = df['CMD_POS_BHG2_YU']
    # encyu = df['ENC_POS_BHG2_YU']
    # cmdalb = df['CMD_POS_BHG2_ALB']
    # encalb = df['ENC_POS_BHG2_ALB']
    # dacalb = df['DAC_BHG2_ALB']
    # errorport = df['BHG2_ALB_ERR_PORT']
    # gfResetCntr = df['GMP_OCA_PORT_40']
    # gfEnableCmdHandler = df['GMP_OCA_PORT_41']
    # gfDisableCmdHandler = df['GMP_OCA_PORT_42']
    # gfResetCmdHandler = df['GMP_OCA_PORT_43']
    
    # t1 = go.Line(x=sample, y=cmdyu, name='CMDPOS_BHY')
    # t2 = go.Line(x=sample, y=cmdalb, name='CMDPOS_ALB')
    # t3 = go.Line(x=sample, y=dacalb, name='DAC_ALB')
    # t4 = go.Line(x=sample, y=errorport, name='ERR_PORT')
    # t5 = go.Line(x=sample, y=gfEnableCmdHandler, name='Enable')
    # t6 = go.Line(x=sample, y=gfDisableCmdHandler, name='Disable')
    # t7 = go.Line(x=sample, y=gfResetCmdHandler, name='Reset')
    
    # fig = make_subplots(rows=6, cols=1, shared_xaxes=True)
    # fig.add_trace(t1,row=1, col=1)
    # fig.add_trace(t2,row=1, col=1)
    # fig.add_trace(t3,row=2, col=1)
    # fig.add_trace(t4,row=3, col=1)
    # fig.add_trace(t5,row=4, col=1)
    # fig.add_trace(t6,row=5, col=1)
    # fig.add_trace(t7,row=6, col=1)
    
    # fig.update_layout(height=1200, width=800)
    # fig.show()
    
    # fig.write_html(os.path.join(workdir,filenames[fileno]+'.html'))

if __name__ == '__main__':
    main()
