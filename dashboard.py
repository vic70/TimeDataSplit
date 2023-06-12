import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


class dataloader:
    def __init__ (self, df):
        self.df = df



def appRun(figure):
    app = Dash(__name__)
    app.layout = html.Div([
        html.Div(children="Data Plotting Ver 1"),
        dcc.Graph(figure=figure)
    ])
    app.run_server(debug=True)


def main():
    appRun()

if __name__ == '__main__':
    main()
