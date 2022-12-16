# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
from statistics import mode
import plotly.express as px

# 2. Create a Dash app instance
app = dash.Dash(
    external_stylesheets=[dbc.themes.SPACELAB],
    name = 'Mental Health - Suicide'
)

app.title = 'Mental Health - Suicide Dashboard Analytics'

## ---- Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
    ],
    brand="Mental Health - Suicide Dashboard Analytics",
    brand_href="#",
    color="light",
)

## --- Import Dataset
s_age=pd.read_csv('s_age.csv')
s_country=pd.read_csv('s_country.csv')
s_gender=pd.read_csv('s_gender.csv')

### CARD CONTENT
total_country = [
    dbc.CardBody([
        html.H1(('98%'),style={'textAlign':'center'}),
        dbc.CardGroup('of those who died by suicide had a diagnosable mental disorder', style={'textAlign':'center'})])
]

total_suicide = [
    dbc.CardBody([
        html.H1([s_country[s_country['year']==2019]['death'].sum()],style={'textAlign':'center'}),
        dbc.CardGroup('Total suicide in 2019', style={'textAlign':'center','display':'inline'}),
        html.Br(),
        html.Br(),
    ]),
]

percent_suicide = [
    dbc.CardBody([
        html.H1([('1.3%')],style={'textAlign':'center'}),
        dbc.CardGroup('of deaths were from suicide in 2019', style={'textAlign':'center','display':'inline'}),
        html.Br(),
        html.Br(),
    ])  
]

## --- Visualization Choropleth
plot_maps=px.choropleth(s_country,
            locations='country_code',
            color_continuous_scale='teal',
            color='death',
            animation_frame='year',
            range_color=[0,75000],
            labels={'country_code':'Country Code','death':'Total Death (Suicide)','year':'Year'},
                       hover_name='country')

## --- Visualization line
plot_line=px.line(s_gender[s_gender['country']=='Indonesia'].sort_values('year'),
    x='year',
    y='val_gender',
    color='gender',
    template = 'ggplot2',
    labels={'gender':'Gender','year':'Year','val_gender':'Suicide Rates'},
    title='Suicide Rates per Gender')

# --- Visualization bar plot
plot_top=px.bar(
    s_country[s_country['year']==2019].sort_values('death').tail(10),
    x = 'death',
    y = 'country',
    template = 'ggplot2',
    title = 'Top 10 Number of Suicide in 2019',
    labels={'death':'Total death (Suicide)','country':'Country'},
    color_discrete_sequence=['#4c78a8'],
)

# --- Visualization histogram
plot_hist=px.bar(
    s_age[s_age['country']=='Indonesia'].sort_values('age'),
    x = 'age',
    y='age_value',
    template = 'ggplot2',
    labels={'age':'Age','age_value':'Suicide Rates'},
    title='Suicide Rates per Age',
    color_discrete_sequence=['#4c78a8'],
)

#### -----LAYOUT-----

app.layout = html.Div([
    navbar,
    html.Br(),

    ## --Component Main Page---

    html.Div([
        ## --ROW1--
        dbc.Row([
            ### COLUMN 1
            dbc.Col([
                    dbc.Card(total_country, className="btn btn-primary disabled"),
                ],
                width=4),
            ### COLUMN 2
            dbc.Col([
                    dbc.Card(total_suicide, className="btn btn-primary disabled"),
                ],width=4),
            ### COLUMN 3
            dbc.Col([
                    dbc.Card(percent_suicide, className="btn btn-primary disabled"), 
                ],width=4),
            ]),
        ## --ROW2--
        dbc.Row([
            ### COLUMN 1
            dbc.Col([
                html.Br(),
                dbc.Card([
                    dbc.CardHeader([html.H6("ABOUT", className='card-title'),]),
                    dbc.CardBody([
                        html.P('Depression and other mood disorders are widely recognized among the most important risk factors for suicide. Bertolote and Fleischmann (2002) report that 98% of those who died by suicide had a diagnosable mental disorder',style={'textAlign':'justify'}),
                        html.P('The World Health Organization (WHO) and the Global Burden of Disease study estimate that almost 800,000 people die from suicide every year, or equal to one person die from suicide every 40 seconds.',style={'textAlign':'justify'}),
                        html.P('In 2019, 1.3% of deaths were from suicide and it makes suicide became the top 15 as the leading cause of death in the world.',style={'textAlign':'justify'}),
                        html.H6('Source :'),
                        dbc.CardLink("Our World in Data", href='https://ourworldindata.org/suicide'),
                        dbc.CardLink('World Health Organization', href='https://www.who.int/data/gho/data/themes/mental-health/suicide-rates',)
                    ]),
                 ])
             ],width=5),
             ### COLUMN 2
            dbc.Col([
                dcc.Graph(figure=plot_maps),
            ],width=7),
                  ]),
        html.Br(),
        ## --ROW3--
        dbc.Row([
            ### COLUMN 1
            dbc.Col([
                html.H3('Analysis by Year '),
                dbc.Card([
                    dbc.CardHeader('Select Year'),
                    dbc.CardBody(
                        dcc.Dropdown(
                            id='choose_year',
                            options=s_country['year'].unique(),
                            value=2019,    
                        ),
                    ),
                ]),
                html.Br(),html.Br(),
                dcc.Graph(
                            id='plotranking',
                            figure='plot_top',
                        )
            ], width=6),
            ### COLUMN 2
            dbc.Col([
                html.H3('Analysis by Country'),
                dbc.Card([
                    dbc.CardHeader('Select Country'),
                    dbc.CardBody(
                        dcc.Dropdown(
                            id='choose_country',
                            options=s_gender['country'].unique(),
                            value='Indonesia',
                        ),
                    ),
                ]),dbc.Tabs([
                    ### TAB 1
                    dbc.Tab(
                    dcc.Graph(
                    id='plotline',
                    figure='plot_line',
                ), label='Gender',
                
                ),
                    ### TAB 2 
                    dbc.Tab(
                        dcc.Graph(
                            id='plotage',
                            figure='plot_hist',
                        ), label='Age-groups'
                    ),
                ]),
            ], width=6),  
        ]),
                       ],style={
        'paddingLeft':'30px',
        'paddingRight':'30px'}),
    ])

### Callback Plot Ranking
@app.callback(
    Output(component_id='plotranking', component_property='figure'),
    Input(component_id='choose_year',component_property='value')
)

def plotrank(year_category):
    plot_top=px.bar(
    s_country[s_country['year']==year_category].sort_values('death').tail(10),
    x = 'death',
    y = 'country',
    template = 'ggplot2',
    title = f'Top 10 Number of Suicide in {year_category}',
    labels={'death':'Total death (Suicide)','country':'Country'},
    color_discrete_sequence=['#4c78a8'],
    )
    return plot_top

### Callback Plot Age
@app.callback(
    Output(component_id='plotage', component_property='figure'),
    Input(component_id='choose_country',component_property='value')
)

def plotage(country_name):
    plot_hist=px.bar(
    s_age[s_age['country']==country_name].sort_values('age'),
    x = 'age',
    y='age_value',
    template = 'ggplot2',
    labels={'age':'Age','age_value':'Suicide Rates'},
    title=f'Suicide Rates per Age in {country_name}',
    color_discrete_sequence=['#4c78a8'],
    )
    return plot_hist

### Callback Plot Line
@app.callback(
    Output(component_id='plotline', component_property='figure'),
    Input(component_id='choose_country',component_property='value')
)

def plotline(country_name):
    plot_line=px.line(s_gender[s_gender['country']==country_name].sort_values('year'),
    x='year',
    y='val_gender',
    color='gender',
    template = 'ggplot2',
    labels={'gender':'Gender','year':'Year','val_gender':'Suicide Rates'},
                 title=f'Suicide Rates per Gender in {country_name}')
    return plot_line
         

     
# 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()