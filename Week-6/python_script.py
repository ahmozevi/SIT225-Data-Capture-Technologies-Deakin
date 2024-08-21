# Loading the Data
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
# Load the data
df = pd.read_csv('gyroscope_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
# Explore the data
print(df.head())
print("Data rows X cols:", df.shape)

# Initialize the Dash app
app = dash.Dash(__name__)
# Layout of the app
app.layout = html.Div([
dcc.Dropdown(
id='graph-type',
options=[
{'label': 'Scatter Plot', 'value': 'scatter'},
{'label': 'Line Chart', 'value': 'line'},
{'label': 'Distribution Plot', 'value': 'histogram'}
],
value='scatter'
),
dcc.Dropdown(
id='data-variable',
options=[
{'label': 'X', 'value': 'X'},
{'label': 'Y', 'value': 'Y'},
{'label': 'Z', 'value': 'Z'},
{'label': 'All', 'value': 'all'}
],
value='X'
),
dcc.Input(id='sample-size', type='number', value=100, min=1),
html.Button('Previous', id='prev-button', n_clicks=0),
html.Button('Next', id='next-button', n_clicks=0),
dcc.Graph(id='graph'),
html.Div(id='data-summary')
])

# Creating Callback Functions
# Callback to update the graph and summary
@app.callback(
[Output('graph', 'figure'),
Output('data-summary', 'children')],
[Input('graph-type', 'value'),
Input('data-variable', 'value'),
Input('sample-size', 'value'),
Input('prev-button', 'n_clicks'),
Input('next-button', 'n_clicks')]
)
def update_graph(graph_type, variable, sample_size, prev_clicks, next_clicks):
# Pagination logic
if 'page' not in update_graph.__dict__:
update_graph.page = 0
num_rows = len(df)
start_index = update_graph.page * sample_size
end_index = min(start_index + sample_size, num_rows)
# Handle previous and next clicks
if prev_clicks > 0:
update_graph.page = max(update_graph.page - 1, 0)
if next_clicks > 0:
update_graph.page = min(update_graph.page + 1, (num_rows - 1) //sample_size)

# Slice the dataframe
df_subset = df[start_index:end_index]
# Create figure based on user selections
if variable == 'all':
df_long = df_subset.melt(id_vars=['timestamp'], value_vars=['X', 'Y',␣
↪'Z'], var_name='Axis', value_name='Value')
if graph_type == 'line':
fig = px.line(df_long, x='timestamp', y='Value', color='Axis')
elif graph_type == 'scatter':
fig = px.scatter(df_long, x='timestamp', y='Value', color='Axis')
else: # histogram
fig = px.histogram(df_long, x='Value', color='Axis')
else:
if graph_type == 'line':
fig = px.line(df_subset, x='timestamp', y=variable)
elif graph_type == 'scatter':
fig = px.scatter(df_subset, x='timestamp', y=variable)
else: # histogram
fig = px.histogram(df_subset, x=variable)
# Create summary table
summary = df_subset.describe(include='all').to_dict()
summary_table = html.Table([
html.Tr([html.Th('Statistic')] + [html.Th(col) for col in summary if col != 'timestamp']),
*[html.Tr([html.Td(stat)] + [html.Td(summary[col].get(stat, 'N/A')) for col in summary if col != 'timestamp'])
for stat in ['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
])
return fig, summary_table

# Running the App
if __name__ == '__main__':
app.run_server(debug=True)