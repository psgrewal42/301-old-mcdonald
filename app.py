import dash 
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
import logging

########### Define your variables ######

# here's the list of possible columns to choose from.
list_of_columns =['code', 'state', 'category', 'total exports', 'beef', 'pork', 'poultry',
       'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh',
       'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton']

mycolumn='corn'
myheading1 = f"Wow! That's a lot of {mycolumn}!"
mygraphtitle = '2011 US Agriculture Exports by State'
mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
mycolorbartitle = "Millions USD"
tabtitle = 'Old McDonald'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/austinlasseter/dash-map-usa-agriculture'


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/usa-2011-agriculture.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1(myheading1),
    dcc.Dropdown(list_of_columns[3:], ['total exports'], id='state-dropdown', multi=True),
    dcc.Graph(
        id='figure-1'
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

@app.callback(dash.dependencies.Output('figure-1', 'figure'),[dash.dependencies.Input('state-dropdown', 'value')])
def create_map(value):
    title = "{} Exports in Millions USD".format(value)
    df['current_total'] = df[value].sum(axis=1)
    fig = go.Figure(data=go.Choropleth(
    			locations=df['code'], # Spatial coordinates
    			z = df['current_total'].astype(float), # Data to be color-coded
    			locationmode = 'USA-states', # set of locations match entries in `locations`
    			colorscale = mycolorscale,
    			colorbar_title =title,
			))

    fig.update_layout(
    	title_text = mygraphtitle,
    	geo_scope='usa',
    	width=1200,
    	height=800
	)
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server()
