import json
import os

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import eli5
import plotly.express as px

from project.load_model import load_model, tokenize
from project.viz import Crosstab

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.title = 'County-Level Poltical Analysis of Coronavirus-Related Tweets'

app.layout = html.Div([

    html.Div([
        html.H1(children='COVID-19 on Twitter'),

        html.Div(children='County-Level Poltical Analysis of Coronavirus-Related Tweets'),

        html.Div([
            dcc.Input(id='input_keyword', type='text', inputMode='latin', required=True),
            html.Button(id='submit_button', n_clicks=0, children='Submit'),
            html.Div(id='output_state')

        ], style={'text_align':'center'})

    ]),

    html.Div([
        html.H3(id='prediction', children='output will go here')
    ]),

    
    html.Div([
        dcc.Graph(id='the_graph')
    ])

])

# --------CALLBACKS--------

@app.callback(
    [Output('prediction', 'children')],
    [Input('submit_button', 'n_clicks')],
    [State(component_id='input_keyword', component_property='value')]
)

def display_prediction(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        model = load_model()
        prediction = model.predict([val_selected])
        return list(prediction)

@app.callback(
    [Output('output_state', 'children'),
     Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_keyword', component_property='value')]
)

def update_weights(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        model = load_model()
        weights = eli5.formatters.as_dataframe.explain_prediction_df(model['bayes'], val_selected, vec=model['counter'], target_names=['Blue', 'Red'])
        weights['color'] = [weights['target'][i]
                            if weights['weight'][i] > 0 
                            else ['Blue', 'Red'][['Blue', 'Red'] != weights['target'][i]]
                            for i in range(len(weights['target']))]
        return (f'You asked the model to predict if "{val_selected}" was most likely tweeted in a Red or Blue County',
                px.bar(weights, x='weight', y='feature', orientation='h', color='color'))

if __name__ == "__main__":
    app.run_server(debug=True)