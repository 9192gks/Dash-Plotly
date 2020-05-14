import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
# from pandas import read_excel
import plotly.io as pio

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash()

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP']

# app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
# app.css.config.serve_locally = False
# app.scripts.config.serve_locally = True

# app = dash.Dash()


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.css.config.serve_locally = False
# app.scripts.config.serve_locally = True

file_name = 'samplePop1.csv'
df = pd.read_csv(file_name)
print(df.head())

colors = {'BLACK' : '#000000','TEXT' :  '#696969','PLOT_COLOR' : '#C0C0C0','WHITE' : '#FFFFFF','GOLD' : '#EEBC35' ,
    'BROWN' : '#53354D' ,'GREEN' : '#42CE90' ,'RED' : '#F87861' ,'YELLOW' : '#F1F145' ,'SKY_BLUE' : '#A3DBE1' ,'SILVER': '#CCCCCC' ,'LIGHT_BLACK' : '#374649'
    }

#status options for dropdown
status_options = []
for status in df['Status'].unique():
    status_options.append({'label':str(status),'value':status})
# print(status_options)

#Pie chart static function
def pop_pie():
    pie_data = df.groupby('Status')['Population Census 1991'].count()
    pie_dataframe = pie_data.to_frame().reset_index()
    trace1 = go.Pie(
                labels = pie_dataframe['Status'].tolist(),
                values= pie_dataframe['Population Census 1991'].tolist(),
                textinfo='label+percent',
                name='population 1991 status wise',pull=[0,0,0,0,0,0,0,0,0]
                )
    data = [trace1]
    layout = go.Layout(
        title='District wise chart',
        height=450,
        width = 666.5,
        paper_bgcolor=colors['LIGHT_BLACK'],
        plot_bgcolor=colors['LIGHT_BLACK'],
        font ={'color' : colors['WHITE'], 'size' : 12},
        legend=dict(
                x=-0.5, y=1.2,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)',
                # orientation="h",
                font=dict( 
                    family="Arial", 
                    size=8, color="white" )
                )
    )
    fig = go.Figure(data=data,layout=layout)
    return fig


app.layout =  dbc.Container(fluid=True,children=[html.Div(
                                dcc.Dropdown(id='status_picker',options=status_options,
                                placeholder="Select Status",
                                    style = {'color' : colors['LIGHT_BLACK'],"background-color": colors['LIGHT_BLACK']},
                                    multi=True,
                                    clearable=True,
                                    searchable=True
                                    ))  ,
        html.Div( className="row",
            children=[
                html.Div(
                    className="six columns",
                    children=[
                        html.Div(
                            children = dcc.Graph(id='Bar-Chart')
                )]),
                html.Div(
                    className="six columns",
                    children=[
                        html.Div(
                            children=dcc.Graph(id='pie-chart', figure=pop_pie())
                )] ) 
        ])])
@app.callback(Output('Bar-Chart','figure'),
                [Input('status_picker','value')])
def update_figure(selected_status):
    print(selected_status)
    if selected_status == [] or selected_status == None:
        trace1 =go.Bar(y=df['Population Census 1991'], 
                            x=df['Name'],name ='1991',
                            marker = {'color' : colors['GREEN']}
                            # orientation='h'
                            )
        trace2 =go.Bar(y=df['Population Census 2001'], 
                            x=df['Name'],name ='2001',
                            marker = {'color' : colors['RED']}
                            # orientation='h'
                            )
        trace3 = go.Bar(y=df['Population Census 2011'], 
                            x=df['Name'],name ='2011',
                            marker = {'color' : colors['YELLOW']}
                            # orientation='h'
                            )
    else:
        filtered_df = df[df['Status'].isin(selected_status)]
        print(filtered_df)
        trace1=go.Bar(y=filtered_df['Population Census 1991'], 
                            x=filtered_df['Name'],name ='1991',
                            marker = {'color' : colors['GREEN']}
                            # orientation='h'
                            )
        trace2=go.Bar(y=filtered_df['Population Census 2001'], 
                            x=filtered_df['Name'],name ='2001',
                            marker = {'color' : colors['RED']}
                            # orientation='h'
                            )
        trace3=go.Bar(y=filtered_df['Population Census 2011'], 
                            x=filtered_df['Name'],name ='2011',
                            marker = {'color' : colors['YELLOW']}
                            # orientation='h'
                            )
    traces= [trace1,trace2,trace3]
    '''
    for status in filtered_df['Status'].unique():
        df_by_status = filtered_df[filtered_df['Status'] == selected_status]
        traces.append(
            go.Bar(y=df_by_status['Population Census 1991'], 
                        x=df_by_status['Name'],name ='1991',
                        marker = {'color' : colors['GREEN']}
                        # orientation='h'
                        ))
        traces.append(
            go.Bar(y=df_by_status['Population Census 2001'], 
                        x=df_by_status['Name'],name ='2001',
                        marker = {'color' : colors['RED']}
                        # orientation='h'
                        ))
        traces.append(go.Bar(y=df_by_status['Population Census 2011'], 
                        x=df_by_status['Name'],name ='2011',
                        marker = {'color' : colors['YELLOW']}
                        # orientation='h'
                        ))'''
    return {
        'data' : traces,
        'layout' : go.Layout(
            title='Population Census',
            height=450,
            width = 666.5,
            # float = 'left',
            paper_bgcolor=colors['LIGHT_BLACK'],
            plot_bgcolor=colors['LIGHT_BLACK'],
            font ={'color' : colors['WHITE']},
            xaxis_tickfont_size=14,
            yaxis=dict(showgrid=False,
                title='Population',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)',
                orientation="h"
                ),
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1, # gap between bars of the same location coordinate.
            xaxis={'categoryorder':'total descending'})
            }

if __name__ == '__main__':
    app.run_server(port =  '8086' , debug ='True')