import json
import os

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import eli5
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

import project.load_model
from project.load_model import load_model

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.title = 'County-Level Poltical Analysis of Coronavirus-Related Tweets'

app.layout = html.Div([

    html.Div([
        html.H1(children='County-Level Poltical Analysis of Coronavirus-Related Tweets'),

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
        
        html.Div([
            dcc.Graph(id='the_graph')
        ], className='six columns'),

        html.Div([
            dcc.Markdown('''
            ## Why This Project?
            
            This project intends to mitigate the spread of Coronavirus by providing to relief organizations a firmer understanding of how political geography affects an individual's reaction to crisis.
            By uncovering the keywords that differentiate Twitter users from Red counties vs Blue counties (based on 2016 Presidential Election results), this model aims to assist public health workers address the needs of individuals based on their political geography.
            ## Interpreting This Graph
            
            Submit a tweet, and a graph will appear that displays the keywords of the tweet that the model believes predicts the political affiliation of the user's county.
            
            ## How Was This Data Sourced?

            This model was trained on 30,000 tweets tweeted during the week of March 30, 2019. They were sourced using Twitter's official API and the Tweepy python library.
            ''')
        ], className='six columns')
    ], className='row')

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
        return [f'A {list(prediction)[0]} County']

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
        target_names = ['Blue', 'Red']
        model = load_model()
        weights = eli5.formatters.as_dataframe.explain_prediction_df(model['lr'], val_selected, vec=model['counter'], target_names=target_names)
        weights['color'] = [weights['target'][i]
                            if weights['weight'][i] > 0 
                            else target_names[target_names != weights['target'][i]]
                            for i in range(len(weights['target']))]
        fig = px.bar(weights, x='weight', y='feature', orientation='h',
                     color='color', color_discrete_map={'Red': 'red', 'Blue': 'blue'})
        fig.update_layout(
            title="Which Keywords Sway a Tweet's Geographical Political Affiliation?",

        )
        return (f'You asked the model to predict if "{val_selected}" was most likely tweeted in a Red or Blue County',
                fig)

if __name__ == "__main__":
    app.run_server()