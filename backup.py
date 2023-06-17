import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

class DashApp:
    def __init__(self, title):
        self.title = title
        self.app = dash.Dash(__name__)
        self.app.title = self.title
        self.figures = []

    def add_figure(self, figure):
        print('Adding figure...')
        self.figures.append(figure)

    # def run(self):
    #     self.app.layout = html.Div([
    #         html.H1(self.title),
    #         *[dcc.Graph(figure=figure) for figure in self.figures]
    #     ])
    #     self.app.run_server(debug=True)


class ScatterPlot(DashApp):
    def __init__(self, df_list):
        super().__init__(title='Scatter Plot')
        self.df_list = df_list
        self.dropdown_options = [{'label': f'{col}', 'value': col} for col in self.df_list.columns]
        self.fig = make_subplots(specs=[[{"secondary_y": True}]], shared_xaxes=True)
        self.fig.update_xaxes(title_text="Time (ms)")
        self.fig.update_yaxes(title_text="")
        

    def create_figure(self):
        print('Creating scatter plot...')
        dropdown = dcc.Dropdown(
            id='dropdown',
            options=self.dropdown_options,
            value=(self.df_list.columns[0], self.df_list.columns[1]),
            multi=True
        )


        @self.app.callback(
            Output('scatter-plot', 'figure'),
            [Input('dropdown', 'value')]
        )
        def update_figure(selected_cols):
            print('Updating scatter plot...')
            if len(selected_cols) <= 1:
                return go.Figure(data=[], layout=go.Layout(title=go.layout.Title(text="Please select at least one column to plot.")))

            fig = make_subplots(specs=[[{"secondary_y": True}]], shared_xaxes=True)

            if len(selected_cols) > 1:
                for idx, selected_value in enumerate(selected_cols):
                    if idx == 0:
                        fig.add_trace(
                            go.Scatter(
                                x=self.df_list.index,
                                y=self.df_list[selected_value],
                                name=selected_value
                            ),
                            secondary_y=False
                        )

                    if idx == 1:
                        fig.add_trace(
                            go.Scatter(
                                x=self.df_list.index,
                                y=self.df_list[selected_value],
                                name=selected_value
                            ),
                            secondary_y=True
                        )
                fig.update_yaxes(title_text=f"<b>{selected_cols[0]}", secondary_y=False)
                fig.update_yaxes(title_text=f"<b>{selected_cols[1]}", secondary_y=True)
                fig.update_layout(title= f"Scatter Plot with {selected_cols[0]} and {selected_cols[1]} across Time (ms)")
                return fig

        self.add_figure(self.fig)
        return dropdown
    
    def run(self, dropdown):
        self.app.layout = html.Div([
            html.H1(self.title),
            dropdown,  # Add the dropdown to the layout
            *[dcc.Graph(id='scatter-plot', figure=self.fig) for _ in range(len(self.figures))]
        ])
        self.app.run_server(debug=True)


# class ScatterPlotApp(DashApp):
#     def __init__(self, title, df_list):
#         super().__init__(title)
#         self.df_list = df_list

#     def create_figures(self):
#         for col in self.df_list.columns:
#             scatter_plot = ScatterPlot(self.df_list)
#             scatter_plot.create_figure()
#             self.add_figure(scatter_plot.fig)
