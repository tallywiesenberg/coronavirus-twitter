import json
import os

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from project.viz import Crosstab

app = dash.Dash()

app.title = 'County-Level Poltical Analysis of Coronavirus-Related Tweets'

app.layout = html.Div(

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        html.H1(children='COVID-19 on Twitter'),

        html.Div(children='County-Level Poltical Analysis of Coronavirus-Related Tweets'),

        html.Div([
            dcc.Input(id='input_keyword', type='text', inputMode='latin', required=True),
            html.Button(id='submit_button', n_clicks=0, children='Submit'),
            html.Div(id='output_state')

        ], style={'text_align':'center'})

    ])


)

# --------CALLBACKS--------

@app.callback(
    [Output(component_id='output_state', component_property='children'),
     Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks'),
     State(component_id='input_state', component_property='value')]
)

def update_graph(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        ct = Crosstab(frac=0.1)
        counties = json.load(os.path.join('data', 'UScounties', 'UScounties.json'))
        full_crosstab = ct.get_crosstab()
        filtered_crosstab = ct.filter(val_selected)
        fig = px.choropleth(filtered_crosstab, geojson=counties, color=filtered_crosstab.values)
        fig.show()

if __name__ == "__main__":
    app.run_server(debug=True)