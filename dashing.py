import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
download_plotlyjs()

# Load the data into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Create a Dash app with a single figure
app = dash.Dash()
fig = go.Figure()

# Define the X and Y series for each scatter plot
x1 = df['X1']
y1 = df['Y1']
x2 = df['X2']
y2 = df['Y2']

# Create a multi-series scatter plot with shared X-axis
fig.add_trace(go.Scatter(x=x1, y=y1), mode='lines')
fig.add_trace(go.Scatter(x=x2, y=y2), mode='lines', line=dict(dash=0))

# Define the dropdown menu options and corresponding values
dropdown = dcc.Dropdown(
    id='dropdown-menu',
    options=[{'label': 'Option 1', 'value': 'option1'}, {'label': 'Option 2', 'value': 'option2'}]
)

# Define the callback function for the dropdown menu selection
@app.callback(
    [Output('fig', 'children'), Input('dropdown-menu', 'value')],
    [State('dropdown-menu', 'value')]
)
def update_plot(selected_option):
    # Update the figure data and layout based on the selected option
    if selected_option == 'option1':
        fig.add_trace(go.Scatter(x=df['X3'], y=df['Y3']), mode='lines')
        fig.update_layout(title='Option 1', xaxis=dict(template='<tspan>{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'
                                                    '{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'
                                                    '{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'))
        fig.update_layout(xaxis=dict(template='<tspan>{{x1}}</tspan><tspan class="axis-label">{{y1}}</tspan>'
                                             '{{x2}}</tspan><tspan class="axis-label">{{y2}}</tspan>'
                                             '{{x3}}</tspan><tspan class="axis-label">{{y3}}</tspan>'))
    elif selected_option == 'option2':
        fig.add_trace(go.Scatter(x=df['X4'], y=df['Y4']), mode='lines')
        fig.update_layout(title='Option 2', xaxis=dict(template='<tspan>{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'
                                                    '{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'
                                                    '{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'))
        fig.update_layout(xaxis=dict(template='<tspan>{{x1}}</tspan><tspan class="axis-label">{{y1}}</tspan>'
                                             '{{x2}}</tspan><tspan class="axis-label">{{y2}}</tspan>'
                                             '{{x3}}</tspan><tspan class="axis-label">{{y3}}</tspan>'))
    else:
        fig.add_trace(go.Scatter(x=df['X5'], y=df['Y5']), mode='lines')
        fig.update_layout(title='Option 3', xaxis=dict(template='<tspan>{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'
                                                    '{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'
                                                    '{{x}}</tspan><tspan class="axis-label">{{y}}</tspan>'))
        fig.update_layout(xaxis=dict(template='<tspan>{{x1}}</tspan><tspan class="axis-label">{{y1}}</tspan>'
                                             '{{x2}}</tspan><tspan class="axis-label">{{y2}}</tspan>'
                                             '{{x3}}</tspan><tspan class="axis-label">{{y3}}</tspan>'))
    return fig