import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.offline import plot
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import quandl
import plotly.figure_factory as ff


#Graph Churn
x_values_1 = ['X8','X7','X6','X5'] 
x_values_2 = ['X4','X3','X2','X1'] 
y_values_1 = [20,15,45,15]
y_values_2 = [-30,-5,-40,-15]
trace_1 = go.Bar(y=x_values_1, x=y_values_1, name="Negative", orientation = 'h', 
    marker=dict(color="rgb(153, 235, 255)",line=dict(color='blue', width=1.5)))
trace_2 = go.Bar(y=x_values_2, x=y_values_2, name="Positive", orientation = 'h', 
    marker=dict(color="rgb(255, 153, 255)",line=dict(color='pink', width=1.5)))

layout1 = dict(    
    title='<b>Correlation with employees probability of churn</b>', 
    yaxis=dict(title='Variable'))
    
data_1 = [trace_1,trace_2]
figure1 = dict(data=data_1,layout=layout1)
churnGraph = dcc.Graph(id="churn_statistics", figure=figure1)

#Graph Roadmap  
df = [dict(Task="Task 1", Start='2018-01-01', Finish='2018-01-31', Resource='Idea Validation'),
      dict(Task="Task 2", Start='2018-03-05', Finish='2018-04-15', Resource='Prototyping'),
      dict(Task="Task 3", Start='2018-04-20', Finish='2018-09-30', Resource='Team Formation')]
colors = ['#0033cc', '#009933', '#e68a00']
fig = ff.create_gantt(df, colors=colors, index_col='Resource', reverse_colors=True, show_colorbar=True, title="Startup Roadmap")
roadmapGraph = dcc.Graph(id="project_roadmap", figure=fig)

#Graph Stocks
quandl.ApiConfig.api_key = "Z2sSmytWEmYixSoCD-yN"
data1=quandl.get("WIKI/AAPL")
data2=quandl.get("BCHARTS/ABUCOINSUSD")
data3=quandl.get("WIKI/MSFT")
data4=quandl.get("WIKI/DIS")
data5=quandl.get("WIKI/GOOGL")

#Graph GDP
gdp = quandl.get("FRED/GDP")
#data_2=[go.Scatter(x=gdp.index, y=gdp.Value, fill ='tozeroy')]
#layout2=dict(title="<b>US GDP Over Time</b>")
#figure2 = dict(data=data_2, layout=layout2)


#Dashboard
app=dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.layout = html.Div([
    
        html.Div([html.Div([html.H1("Homework 5", style={"color":"#6666ff", "text-align":"center", "font-family":"cursive"})], className="twelve columns")], className="row"),
        html.Div([
            html.Div([
            dcc.RadioItems(
            id = 'radiobutton',
            options=[
                {'label': 'Employee Churn', 'value': 1},
                {'label': 'Startup RoadMap', 'value': 2}
                ],
            ),
        ], className='three columns'),
       
        html.Div([], id = 'graph_container_div',className='nine columns')
    ],
    className='row'),

#Stocks
        html.Div([
            dcc.Dropdown(
        id = 'option_in_2',
        options=[
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'BitCoin', 'value': 'ABUCOINSUSD'},
            {'label': 'Microsoft', 'value': 'MSFT'},
            {'label': 'Disney', 'value': 'DIS'},
            {'label': 'Google', 'value': 'GOOGL'}             
            
        ],
        multi=True,
        placeholder="Please, select a stock"),
    html.Div([], id = "graph2", className = 'nine columns')
        ],
        className='row'),
          
#Slider
    html.Div([
            html.Div([
                dcc.Graph(id='graph_slider'),
                
                dcc.RangeSlider(
                id = 'option_in_3',min=0,max=len(gdp.index),step =0.5,value=[0, len(gdp.index)]),
            ])  
    ],
    className='row')
],
className = 'row')

#Callbacks

@app.callback(
    Output(component_id='graph_container_div', component_property='children'),
    [Input(component_id='radiobutton', component_property='value')],
    )
def update_graph(input_value):
    if input_value==1:
        return churnGraph
    elif input_value==2:
        return roadmapGraph        

@app.callback(
    Output(component_id='graph2', component_property='children'),
    [Input(component_id='option_in_2', component_property='value')]
)
def update_graph(stocks):
    headerArray = []
    cellsArray = []
    boxData = []
    if len(stocks) > 0 and len(stocks)< 3:
        for value in stocks:
            if(value=='AAPL'):
                headerArray.append('Apple')
                cellsArray.append(round(data1.Open.pct_change()[1:5,],3))
                boxData.append(go.Box(x=data1.Open.pct_change(), name = 'Apple'))
            elif(value=='ABUCOINSUSD'):
                headerArray.append('BitCoin')
                cellsArray.append(round(data2.Open.pct_change()[1:5,],3))
                boxData.append(go.Box(x=data2.Open.pct_change(), name = 'BitCoin'))
            elif(value=='MSFT'):
                headerArray.append('Microsoft')
                cellsArray.append(round(data3.Open.pct_change()[1:5,],3))
                boxData.append(go.Box(x=data3.Open.pct_change(), name = 'Microsoft'))
            elif(value=='DIS'):
                headerArray.append('Disney')
                cellsArray.append(round(data4.Open.pct_change()[1:5,],3))
                boxData.append(go.Box(x=data4.Open.pct_change(), name = 'Disney'))
            elif(value=='GOOGL'):
                headerArray.append('Google')
                cellsArray.append(round(data5.Open.pct_change()[1:5,],3))
                boxData.append(go.Box(x=data5.Open.pct_change(), name = 'Google'))
        
        parentDiv = html.Div([getBox(boxData), getTable(headerArray, cellsArray)], className='row' )
        return parentDiv
    elif(len(stocks) >= 3): return parentDiv
    else: return  'Choose only 2 stocks.'

def getBox(boxData):
    boxLayout = dict(title = 'Distribution of Price churn')
    boxFigure = dict(data=boxData, layout=boxLayout)
    box = dcc.Graph(id="box", figure=boxFigure)
    return box

def getTable(headerArray, cellsArray):

    header = dict(values=headerArray,
              align = ['left','left'],
              font = dict(color = 'white', size = 12),
              fill = dict(color='#ff66cc')
             )
    cells = dict(values=cellsArray,
             align = ['left','left'],
             fill = dict(color=["yellow","white"])
            )  

    trace = go.Table(header=header, cells=cells)
    data = [trace]
    layout = dict(width=500, height=300)
    figure = dict(data=data, layout=layout)
    table = dcc.Graph(id="google_bitcoin_statistics_table", figure=figure)
    return table

@app.callback(
    Output(component_id='graph_slider', component_property='figure'),
    [Input(component_id='option_in_3', component_property='value')]
)
def update_graph(input_value_slider):
    modified_index = gdp.index[input_value_slider[0]:input_value_slider[1]]
    modified_values = gdp.Value[input_value_slider[0]:input_value_slider[1]]
    data = [go.Scatter(x=modified_index,y=modified_values,fill="tozeroy")]
    layout = dict(title = '<b>US GDP over time</b>')
    figure = dict(data=data, layout = layout)
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)