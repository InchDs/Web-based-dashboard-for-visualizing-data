import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data from a CSV file
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# Dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
year_list = list(range(1980, 2024))

# App layout
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard", style={'text-align': 'center', 'color': '#FFFFFF', 'bold': True}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(id='stat-type', options=dropdown_options, value='Yearly Statistics')
    ]),
    html.Div(dcc.Dropdown(id='select-year', options=[{'label': i, 'value': i} for i in year_list], value=2006)),
    html.Div([html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})])
])

# Callback to enable/disable the year selection dropdown based on the selected statistics type
@app.callback(
    Output('select-year', 'disabled'),
    Input('stat-type', 'value'))
def update_input_container(selected_statistics):
    """
    Enable or disable the year selection dropdown based on the selected statistics type.

    Parameters:
    selected_statistics (str): The selected statistics type.

    Returns:
    bool: True if the selected statistics type is not 'Yearly Statistics', False otherwise.
    """
    return selected_statistics != 'Yearly Statistics'

# Callback to update the output container with the appropriate charts based on the selected year and statistics type
@app.callback(
    Output('output-container', 'children'),
    [Input('select-year', 'value'), Input('stat-type', 'value')])
def update_output_container(input_year, stat_type):
    """
    Update the output container with the appropriate charts based on the selected year and statistics type.

    Parameters:
    input_year (int): The selected year.
    stat_type (str): The selected statistics type.

    Returns:
    list: A list of HTML Div elements containing the charts.
    """
    if stat_type == 'Recession Period Statistics':
        # Filter data for recession periods
        recession_data = data[data['Recession'] == 1]
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].count().reset_index()
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        df = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].sum().reset_index()

        return [
            html.Div(className='chart-item', children=[
                dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period")),
                dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average number of Vehicles sold'))
            ]),
            html.Div(className='chart-item', children=[
                dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names="Vehicle_Type", title='Total Expenditure by Vehicle Type')),
                dcc.Graph(figure=px.bar(df, x='unemployment_rate', y="Automobile_Sales", color='Vehicle_Type', title='Effect of Unemployment Rate on Sales'))
            ])
        ]
    elif input_year and stat_type == 'Yearly Statistics':
        # Filter data for the selected year
        yearly_data = data[data['Year'] == int(input_year)]
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        month = yearly_data.groupby('Month')['Automobile_Sales'].sum().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']).reset_index()
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].count().reset_index()
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        return [
            html.Div(className='chart-item', children=[
                dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Automobile Sales for the year')),
                dcc.Graph(figure=px.line(month, x='Month', y='Automobile_Sales', title=f'Monthly sale for the year {input_year}'))
            ]),
            html.Div(className='chart-item', children=[
                dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title='Average Number of Vehicles Sold')),
                dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Expenditure on each vehicle'))
            ])
        ]
    return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)