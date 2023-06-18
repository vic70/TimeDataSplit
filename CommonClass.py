import  CommonUtil
import tkinter as tk
from tkinter import filedialog

class Config:
    def __init__(self, config_dict):
        self.multiFileInput = config_dict['multiFileSupport']['Input']
        self.multiFileOutput = config_dict['multiFileSupport']['Output']
        self.channelmode = config_dict['splitCondition']['channelmode']
        self.splitmode = config_dict['splitCondition']['splitmode']
        self.splitAtEnd = config_dict['splitCondition']['splitAtEnd']
        self.ahead = config_dict['data_range']['ahead']
        self.behind = config_dict['data_range']['behind']
        self.conditionExist = config_dict['condition']['conditionExist']
        self.conditionalChannel = config_dict['condition']['conditionalChannel']
        self.conditionValue = config_dict['condition']['conditionValue']
        self.plotlist = config_dict['plotChannel']['plotlist']
        self.multiFileSupport = config_dict['multiFileSupport']['Input']
        self.requireFunc = config_dict['function']['requireFunc']
        self.applyChName = config_dict['function']['applyChName']
        self.newChName = config_dict['function']['newChName']
        self.funcs = [getattr(CommonUtil, i) for i in config_dict['function']['funcs']]
        self.funcsInputs = config_dict['function']['funcsInput']

class FileSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Selector")
        self.config_file = None
        self.data_files = None
        self.multi_file_flag = None

    def select_config_file(self):
        self.config_file = filedialog.askopenfilename(initialdir = "__FILE__" ,title = "Select Config File", filetypes = [(("config files","*.cfg"),("all files","*.*"))])
        if self.config_file:
            print(f"Config file selected: {self.config_file}")
        else:
            print("No config file selected.")

    def select_data_files(self):
        if self.multi_file_flag.get() == 1:
            self.data_files = filedialog.askopenfilenames(initialdir = "__FILE__" ,title = "Select Data Files", filetypes = [(("data files","*.dat"),("all files","*.*"))])
        else:
            self.data_files = filedialog.askopenfilename(initialdir = "__FILE__" ,title = "Select Data File", filetypes = [(("data files","*.dat"),("all files","*.*"))])
        if self.data_files:
            print(f"Data file(s) selected: {self.data_files}")
        else:
            print("No data file(s) selected.")

    def confirm_selection(self):
        if self.config_file and self.data_files:
            self.root.quit()
            self.root.destroy()
        else:
            print("Please select both a config file and data file(s) before confirming.")

    def create_ui(self):
        tk.Button(self.root, text='Select Config File', command=self.select_config_file).pack()
        self.multi_file_flag = tk.IntVar()
        tk.Checkbutton(self.root, text='Multiple Data Files?', variable=self.multi_file_flag).pack()
        tk.Button(self.root, text='Select Data File(s)', command=self.select_data_files).pack()
        tk.Button(self.root, text='Confirm Selection', command=self.confirm_selection).pack()
        self.root.mainloop()

    def get_files(self):
        return self.config_file, self.data_files
 