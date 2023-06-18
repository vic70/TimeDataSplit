def getfile_gui():
    window = tk.Tk()
    
    root = tk.Tk()
    root.withdraw()

    config_file = None
    data_file = None

    # create a tkinter window
    window = tk.Toplevel(root)
    window.title("Select Files")

    # create a label for the config file
    config_label = tk.Label(window, text="Select Config File:")
    config_label.grid(row=0, column=0)

    # create an entry widget for the config file
    config_entry = tk.Entry(window, width=50)
    config_entry.grid(row=0, column=1)

    # create a button to select the config file
    def select_config_file():
        config_file = filedialog.askopenfilename(initialdir="__FILE__", title="Select yml config",
                                                 filetypes=[(("yaml file", "*.yml"))])
        config_entry.delete(0, tk.END)
        config_entry.insert(0, config_file)

    config_button = tk.Button(window, text="Select", command=select_config_file)
    config_button.grid(row=0, column=2)

    # create a label for the data file
    data_label = tk.Label(window, text="Select Data File(s):")
    data_label.grid(row=1, column=0)

    # create an entry widget for the data file(s)
    data_entry = tk.Entry(window, width=50)
    data_entry.grid(row=1, column=1)

    # create a button to select the data file(s)
    def select_data_file():
        if multi_var.get():
            data_file = filedialog.askopenfilenames(initialdir="__FILE__", title="Select data log",
                                                    filetypes=[(("text file", "*.txt"))])
        else:
            data_file = filedialog.askopenfilename(initialdir="__FILE__", title="Select data log",
                                                    filetypes=[(("text file", "*.txt"))])
        data_entry.delete(0, tk.END)
        data_entry.insert(0, data_file)

    data_button = tk.Button(window, text="Select", command=select_data_file)
    data_button.grid(row=1, column=2)

    # create a checkbox to enable multi-file selection
    multi_var = tk.BooleanVar()
    multi_checkbox = tk.Checkbutton(window, text="Select Multiple Files", variable=multi_var)
    multi_checkbox.grid(row=2, column=1)
    
    def ok_button():
        nonlocal config_file, data_file
        config_file = config_entry.get()
        data_file = data_entry.get()
        if config_file == '' or data_file == '':
            # display an error message if either file has not been selected
            error_label = tk.Label(window, text="Please select both the config file and data file(s).")
            error_label.grid(row=3, column=1)
            return None, None  # return a tuple of None values
        else:
            window.destroy()

    
    # create an OK button to close the window and return the selected files
    ok_button = tk.Button(window, text="OK", command=ok_button)
    ok_button.grid(row=3, column=1)

    # display the window
    window.mainloop()
    return config_file, data_file