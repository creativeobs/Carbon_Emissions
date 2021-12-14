import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__, meta_tags=[{'name':'viewport', 'content':'width=device-width'}])
app.title = 'Dashboard Co2 Emissions Globally'
server = app.server

df = pd.read_csv('clean_dataset_co2.csv')


app.layout = html.Div([
    
    html.Div(
        [
            
        ], className = 'circle1'
    ),
    
    html.Div(
        [
            
        ], className = 'circle2'
    ),
    
     html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            
                            html.H3('Country:'),
                            html.Br(),
                                
                            dcc.Dropdown(
                                id="dropdown",
                                options=[{"label": x, "value": x} for x in df['Country'].unique()],
                                value=[],
                                clearable=False,
                                multi = True
                            ),
                            html.Br(),
                            
                            html.H3('Type of Carbon Emission:'),
                            html.Br(),
                            dcc.Dropdown(
                                id="dropdown_type",
                                options=[{"label": x, "value": x} for x in df.columns[2:8]],
                                value=df.columns[2],
                                clearable=False,
                            ),
                            html.Br(),
                            html.H3('Year:'),
                            dcc.RangeSlider(
                                id='year-slider',
                                min=1750,
                                max=2015,
                                vertical=True,
                                verticalHeight=570,
                                value=[df['Year'].min(), df['Year'].max()],
                                marks={str(Year): str(Year) for Year in [x for x in range(1750, 2016, 8)]},
                                step= None
                            )
                        ], className='controls_container'
                    ),   
                ], className = 'navbar'
                
                ),
                
            html.Div(
        [
            
            html.Div(
                [
                    html.H2(id='title4'),
                    ], className = 'title_text'
                ),
            
            html.Div(
                [   
             
            html.Div(
                [
                     html.Br(),
                     html.Br(),
                     html.H3(id='t1'),
                     html.H2('Total Carbon Emissions')
                ], className='total_container'
                ),
            
            html.Div(
                [
                    
                    html.Div(
                        [   
                            html.Div(
                                [
                                    html.H3(id='t2'),
                                    html.H2('Solid Fuel'),                   
                                ], className='card_container', style ={'width':'280px'}
                            ),
                    
                            html.Div(
                                [
                                     html.H3(id='t3'),
                                    html.H2('Liquid Fuel'),
                                ], className='card_container', style ={'width':'280px'}
                            ),
                            
                            html.Div(
                                [
                                    html.H3(id='t4'),
                                    html.H2('Gas Fuel'),      
                                 ], className='card_container', style ={'width':'280px'}
                            ),                                                 
                            
                            ], className='flex_container'
                    ),
                    
                    html.Br(),
           
                    html.Div(
                        [   
                            html.Div(
                                [
                                    html.H3(id='t5'),
                                    html.H2('Cement'),               
                                 ], className='card_container', style ={'width':'280px'}
                            ),
                            
                            html.Div(
                                [
                                    html.H3(id='t6'),
                                    html.H2('Gas Flare'),                    
                                ], className='card_container', style ={'width':'280px'}
                            ), 
                            
                            html.Div(
                                [
                                    html.H3(id='t7'),
                                    html.H2('Per Capita'),          
                                 ], className='card_container', style ={'width':'280px'}
                                
                            )
                            
                            
                            ], className='flex_container'
                    ),
                     
                ],
                ),
            
                ], className='data_containter'
            ),   
            
            html.Br(),   
            
            html.Div([
        
                html.Div([
                    html.H3(id='title'),
                    html.Br(),
                    dcc.Graph(
                        id='line',
                        style = {'width':'100%'}
                    )], className= 'content_container', style = {'width':'60%'}
                ),
                
                html.Div([
                   html.H3(id='title5'),
                   dcc.Graph(
                        id='donut',
                    )], className= 'content_container', style = {'width':'30%'}
                ) 
                    
                ], className = 'main_content'
            ),
            
            html.Br(),   
            
            html.Div([
        
        html.Div([
             html.H3(id = 'title2'),
             html.Br(),
             dcc.Graph(
                 id='map',
                 style = {'width':'100%'}
             )
            
        ], className = 'content_container', style = {'width':'93%',
                                                     'margin-bottom': '20px',
                                                     'height': '50%'}
                                                     
        ),
        
        html.Div([
             html.H3(id='title3'),    
             html.Br(),
             dcc.Dropdown(
                id="dropdown_rank",
                options=[{"label": x, "value": x} for x in ['Top 5', 'Top 10', 'Top 20', 'Least 5', 'Least 10', 'Least 20']],
                value='Top 5',
                clearable=False,
            ),
             
             html.Br(),
             
             dcc.Graph(
                 id='bar',
                 style = {'width':'100%'}
             )
            
        ], className = 'content_container', style = {'width':'93%',
                                                     'height': '550px'}      
        )
        
        ], className = 'main_content'
    ),
                                                     
    html.Br(),
           
        ], className='glass'
    ),    
            
        ], className = 'data_container2'
    ),
                
 
     
    
])

@app.callback(
    Output("bar", "figure"), 
    [Input("dropdown_rank", "value"),
     Input('year-slider', 'value'),
     Input('dropdown_type', 'value'),
     Input("dropdown", "value"),
     ])
def update_bar_chart(top, year, dtype, country):
    
    if len(country) == 0:
        country = df['Country'].unique()
        
    mask = df[df['Country'].isin(country)]
    
    ndf = mask[(mask['Year'] >= int(year[0])) & (mask['Year'] <= int(year[1]))]
    
    num = int(top.split()[1])
    
    
    nndf = ndf[['Country', dtype]]
    
    nndf[dtype] = nndf[dtype].apply(lambda x: 0 if x < 0 else x)
    
    if top.split()[0] == 'Top':
        nndf = nndf.groupby('Country').sum().sort_values(dtype, ascending=False).head(num)
    else:
        nndf = nndf.groupby('Country').sum().sort_values(dtype, ascending=True).head(num)
    
    fig4 = px.bar(nndf, y=nndf.index, x=dtype, height=400,
              color=nndf.index).update_layout({
                                            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                            })
    fig4.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig4.update_layout(transition_duration=500)

    return fig4

@app.callback(
    Output("line", "figure"), 
    [Input("dropdown", "value"),
     Input('year-slider', 'value'),
     Input('dropdown_type', 'value')
     ])

def update_line_chart(country, year, dtype):
    
    if len(country) == 0:
        country = df['Country'].unique()
        
    ndf = df[(df['Year'] >= int(year[0])) & (df['Year'] <= int(year[1]))]
        
    mask = ndf[ndf['Country'].isin(country)]
    
    fig = px.line(mask, x="Year", 
                  y=dtype, 
                  color='Country',
                  height= 420,
                  hover_name='Country',
                  ).update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })
                      
    fig.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig.update_layout(transition_duration=500)

    return fig 

@app.callback(
    Output("donut", "figure"), 
    [Input("dropdown", "value"),
     Input('year-slider', 'value'),
     Input('dropdown_type', 'value')
     ])

def update_donut_chart(country, year, dtype):
    
    if len(country) == 0:
        country = df['Country'].unique()
        
    ndf = df[(df['Year'] >= int(year[0])) & (df['Year'] <= int(year[1]))].copy()
        
    mask = ndf[ndf['Country'].isin(country)]
        
    if dtype == 'Total Carbon Emission':
        columns = mask.columns[3:8]
        values = [mask[x].sum() for x in columns]
    else:
        columns = mask.columns[3:8].tolist()
        solo = columns.index(dtype)
        values = [mask[dtype].sum() if x==solo else 0 for x in range(5)]

    
    fig2 = px.pie(mask, columns, values, hole=0.5).update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    
    fig2.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig2.update_layout(transition_duration=500)
    
    return fig2    

@app.callback(
    [Output("title", "children"),
     Output("title2", "children"),
     Output("title3", "children"),
     Output("title4", "children"),
     Output("title5", "children"),
     ], 
    [Input('year-slider', 'value'),
     Input('dropdown_type', 'value'),
     Input('dropdown_rank', 'value')]
    )
def update_title(year, dtype, rank):
    
    return f'Carbon Emissions of Country over Time ({year[0]}-{year[1]}) ({dtype})', f'Global Map of Carbon Emissions over Time ({year[0]}-{year[1]}) ({dtype})', f'{rank.split()[0]} Countries for Carbon Emission ({year[0]}-{year[1]}) ({dtype})', f'Carbon Emissions per Country ({year[0]}-{year[1]})', f'Total Sum percentages of Types of Carbon Emitted ({year[0]}-{year[1]}) ({dtype})'

@app.callback(
    [Output("t1", "children"),
     Output("t2", "children"),
     Output("t3", "children"),
     Output("t4", "children"),
     Output("t5", "children"),
     Output("t6", "children"),
     Output("t7", "children")
     ], 
    [Input("dropdown", "value"),
     Input('year-slider', 'value')
     ])
def update_cards(country, year):
    
    if(len(country)) == 0:
        country = df['Country'].unique()
    
    ndf = df[(df['Year'] >= int(year[0])) & (df['Year'] <= int(year[1]))].copy()
    mask = ndf[ndf['Country'].isin(country)]
    
    t1 = mask['Total Carbon Emission'].sum()
    t2 = mask['Solid Fuel'].sum()
    t3 = mask['Liquid Fuel'].sum()
    t4 = mask['Gas Fuel'].sum()
    t5 = mask['Cement'].sum()
    t6 = mask['Gas Flare'].sum()
    t7 = mask['Per Capita'].sum()
    
    tc7 = '{:.2f}'.format(t7)
    return t1,t2,t3,t4,t5,t6,tc7

@app.callback(
    Output("map", "figure"), 
    [Input("dropdown", "value"),
     Input('year-slider', 'value'),
     Input('dropdown_type', 'value')
     ])

def update_mapbox_chart(country, year, dtype):
    
    
    if len(country) == 0:
        country = df['Country'].unique()
        
    ndf = df[(df['Year'] >= int(year[0])) & (df['Year'] <= int(year[1]))]
        
    mask = ndf[ndf['Country'].isin(country)]
    
    mask['scaled_total'] = mask[dtype].apply(lambda x: 0 if x < 0 else x)
    
    
    
    fig3 = px.scatter_mapbox(mask, hover_name='Country', lat="lat", lon="lon", 
                             color=dtype,
                             size = 'scaled_total', 
                             mapbox_style="carto-positron", 
                             height=500,
                             width = 1250,
                             color_continuous_scale=px.colors.sequential.Rainbow, size_max=30, zoom=1).update_layout({
                                                                                            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                                            })
                                 
    fig3.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig3.update_layout(transition_duration=500)

    return fig3





if __name__ == '__main__':
    app.run_server(debug=True)
