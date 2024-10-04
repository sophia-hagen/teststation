import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.express as px
from flask import Flask
import pandas as pd

# Assuming the existence of a CSV file that gets updated with live data.
csv_file_path = 'C:\\Users\\Constantin\\Documents\\5BHEL\\Diplomarbeit\\DashboardSTS1\\udp_data.csv'

# Flask server and Dash app initialization
# Initialization
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# MQTT Setup
# mqtt_client = CustomMQTTClient("192.168.250.116")
# mqtt_client.connect()
# mqtt_client.start_loop()

# App layout with dynamic graph container
app.layout = html.Div([
    dcc.Store(id='stored-time-range'),
    html.Div([html.H1('Sensor Data Dashboard')], className='header'),
    dcc.Interval(id='update-interval', interval=5000, n_intervals=0),  # Update every 5 seconds

    html.Div([
      html.Div([#Switch for Power Adapter
        html.Div('Power Adapter', className='switch-text'),
        dcc.Checklist(
            id='switch-poweradapter',
            options=[{'label': '', 'value': 'PA'}],
            value=[],
            inputClassName='switch-input',  
            labelClassName='switch-label'
        )
    ],className='switch-wrapper'),
    html.Div([ #Switch for Fans
        html.Div('Fans', className='switch-text'),
        dcc.Checklist(
            id='switch-fans',
            options=[{'label': '', 'value': 'F'}],
            value=[],
            inputClassName='switch-input',  
            labelClassName='switch-label'
        )
    ],className='switch-wrapper'),
    html.Div([ #Switch for Motor
        html.Div('Motor Power', className='switch-text'),
        dcc.Checklist(
            id='switch-motor',
            options=[{'label': '', 'value': 'M'}],
            value=[],
            inputClassName='switch-input',  
            labelClassName='switch-label'
        )
    ],className='switch-wrapper'),
    html.Div([ #Switch for Cooler
        html.Div('Cooler', className='switch-text'),
        dcc.Checklist(
            id='switch-cooler',
            options=[{'label': '', 'value': 'C'}],
            value=[],
            inputClassName='switch-input',  
            labelClassName='switch-label'
        )
    ],className='switch-wrapper'),
    html.Div([ #Switch for LEDs
        html.Div('LEDs', className='switch-text'),
        dcc.Checklist(
            id='switch-leds',
            options=[{'label': '', 'value': 'L'}],
            value=[],
            inputClassName='switch-input',  # Custom class for the input element
            labelClassName='switch-label'
        )
    ],className='switch-wrapper'),
    html.Div([ #Switch for UV-Lamp
        html.Div('UV-Lamp', className='switch-text'),
        dcc.Checklist(
            id='switch-uvlamp',
            options=[{'label': '', 'value': 'U'}],
            value=[],
            inputClassName='switch-input',
            labelClassName='switch-label'
        )
    ],className='switch-wrapper'),  
    ],className='switches-container'),
    dcc.DatePickerRange(
        id='time-range-selector',
        start_date_placeholder_text="Start Date",
        end_date_placeholder_text="End Date",
        calendar_orientation='horizontal',
    ),
    html.Div(id='graphs-container')
])

def generate_figure(dataframe, x_column, y_column, title):
    if dataframe.empty:
        raise ValueError("The dataframe is empty. No data to plot.")

    # Check if the specified columns exist in the dataframe
    if x_column not in dataframe.columns or not any(col in y_column for col in dataframe.columns):
        raise ValueError(f"Specified columns are not in the dataframe. Available columns: {dataframe.columns}")

    # Plotly Express to generate the figure with a default line color for visibility
    if isinstance(y_column, list):  # Check if multiple y_columns are provided for multiple traces
        fig = px.line(dataframe, x=x_column, y=y_column, title=title,
                      color_discrete_sequence=px.colors.qualitative.Plotly)  # Ensuring visibility
    else:
        fig = px.line(dataframe, x=x_column, y=y_column, title=title, labels={y_column: y_column},
                      color_discrete_sequence=px.colors.qualitative.Plotly)  # Ensuring visibility

    # Update the figure with a custom layout
    fig.update_layout(
        plot_bgcolor='#002533',  # Dark background inside the plot area
        paper_bgcolor='#00171f',  # Dark background around the plot area
        font_color='white',  # White text for better visibility
        title_font_color='white',  # Title color
        legend_title_font_color='white',  # Legend title color
        xaxis_title_font_color='white',  # X-axis title color
        yaxis_title_font_color='white',  # Y-axis title color
        xaxis_color='#6e6d6c',  # X-axis tick colors
        yaxis_color='#6e6d6c',  # Y-axis tick colors
        xaxis_tickangle=-45,  # X-axis tick angle
        margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins to fit your layout
        legend=dict(
            yanchor="bottom", 
            y=0.01,
            xanchor="right", 
            x=0.99,
            bgcolor='rgba(0,0,0,0)'  # Transparent legend background
        ),
        hovermode='x unified'  # Unified hover for better readability
    )

    # Return the updated figure
    return fig

# Callback um die graphen, basierend auf die zeit, zu aktualisieren 
@app.callback(
    Output('stored-time-range', 'data'), #Ausgang gespeichert
    [Input('time-range-selector', 'start_date'), #Eingang: Startdatum
     Input('time-range-selector', 'end_date')], #Ausgang: Enddatum
    prevent_initial_call=True #nicht beim ersten mal laden
)
def update_stored_time_range(start_date, end_date):
    return {'start_date': start_date, 'end_date': end_date}


# Callback to update the graphs based on the selected time range
@app.callback(
    Output('graphs-container', 'children'), #Ausgang: alle Eigenschaften des 'graphs-container'
    [Input('update-interval', 'n_intervals')], #Eingang: Timer
    [State('stored-time-range', 'data'), #States der Schalter 
     State('switch-poweradapter', 'value'),
     State('switch-fans', 'value'),
     State('switch-motor', 'value'),
     State('switch-cooler', 'value'),
     State('switch-leds', 'value'),
     State('switch-uvlamp', 'value')]
     
)
def update_graphs(n_intervals, stored_time_range, *args):
    if not stored_time_range:
        return []  # If there's no date range selected, return empty list to avoid error

    print("Update called at interval:", n_intervals)  # Debug: Print the update interval count

    start_date, end_date = stored_time_range.get('start_date'), stored_time_range.get('end_date')
    df = pd.read_csv(csv_file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Debug: Print the DataFrame
    print(df.head())

    # Filter the DataFrame based on the stored date range
    if start_date and end_date:
        filtered_df = df[(df['Timestamp'] >= start_date) & (df['Timestamp'] <= end_date)]
    else:
        filtered_df = df

    # Debug: Print the filtered DataFrame
    print(filtered_df.head())

    if filtered_df.empty:
        return html.Div("No data available for the selected date range.")
    
    # Generate figures for each sensor data
    graphs = [
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', 'Temperature (BME688)', 'Temperature (BME688)')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', 'Temperature (TMP112)', 'Temperature (TMP112)')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', 'Humidity', 'Humidity')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', 'Pressure', 'Pressure')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', 'Gas Resistance', 'Gas Resistance')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', ['Acceleration X', 'Acceleration Y', 'Acceleration Z'], 'Acceleration')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', ['Gyroscope X', 'Gyroscope Y', 'Gyroscope Z'], 'Gyroscope')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', 'UVA', 'UVA')),
        dcc.Graph(figure=generate_figure(filtered_df, 'Timestamp', 'UVA Index', 'UVA Index'))
    ]

    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)