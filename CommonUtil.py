import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Modifying function

def ADC_convert(input, factor = 10, num_bits = 16):
    input_int = input.astype(int)
    mask = 2 ** (num_bits - 1)
    a = -(input_int & mask) # For debug only
    b = (input_int & ~mask) # For debug only
    out = (a + b) * factor
    return out

def convertRes(input, Res = 0.5):
   Out = input * Res
   return Out



#############################################################
# deprecated function for backward compatibility
'''

def create_scatter_plots(df_list):
    app = dash.Dash(__name__)

    # Create dropdown options from DataFrame columns
    dropdown_options = [{'label': f'{col}', 'value': col} for col in df_list.columns]

    app.layout = html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=dropdown_options,
            value=(df_list.columns[0],df_list.columns[0] ),
            multi= True
        ),
        dcc.Graph(id='scatter-plot')
    ])

    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('dropdown', 'value')]
    )
    def update_figure(selected_cols):
        
        if len(selected_cols) <= 1:
         return go.Figure(data=[], layout=go.Layout(title=go.layout.Title(text="Please select at two column to plot.")))
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        if len(selected_cols) > 1:
         for idx, selected_value in enumerate(selected_cols):
               if idx == 0:
                  fig.add_trace(
                     go.Scatter(
                           x=df_list.index,
                           y=df_list[selected_value],
                           name=selected_value
                     ),
                     secondary_y=False
                  )

               if idx == 1:
                  fig.add_trace(
                     go.Scatter(
                           x=df_list.index,
                           y=df_list[selected_value],
                           name=selected_value
                     ),
                     secondary_y=True
                  )
         fig.update_yaxes(title_text=f"<b>{selected_cols[0]}", secondary_y=False)
         fig.update_yaxes(title_text=f"<b>{selected_cols[1]}", secondary_y=True)
         fig.update_layout(title= f"Scatter Plot with {selected_cols[0]} and {selected_cols[1]} across Time (ms)")

        return fig

    return app

'''
'''
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
# def readyml():
#    filepath, filelocation, filename = getfile(title= "Select yml config",filetypes = [(("yaml file","*.yml"))])
#    with open(filepath, 'r') as file:
#       configData = yaml.safe_load(file)
   
#    return configData
'''


