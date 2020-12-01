import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.offline as pyo
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
pyo.init_notebook_mode() ## ensures that the plotly graphics convert to HTML
%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
context='''
The gender wage gap refers to the difference in income between men and women, relative to the income of men, for the same labor. Different studies over time have produced different figures for how drastic the gap in income can be, but a commonly-accepted statistic is that women who work full-time make about 80% of what full-time working men make (in the United States). This wage gap affects women not only while working, but in paying back their debts, saving for retirement, and in the dignity of their work. More information can be found at the website for the American Association of University Women (AAUW): https://www.aauw.org/resources/research/simple-truth/.  

The General Social Survey (GSS) is a survey which aims to study and understand trends in American socioeconomic development through data collection. The survey has been conducted annually or semiannually since 1972, and is widely regarded as a foremost source of data about American society. Primarily run by NORC at the University of Chicago, with principal investigators from a number of leading research institutions, the GSS seeks to provide scholars both within and without the United States with data from which to conduct sociological and attitudinal research. The data are collected by surveying Americans, and the sampling procedure can be found in detail here: https://gss.norc.org/documents/codebook/GSS_Codebook_AppendixA.pdf. Additional information on the GSS can be found on the GSS website: https://gss.norc.org/About-The-GSS.
'''
gss_table = gss_clean[['income', 'job_prestige', 'socioeconomic_index', 'education', 'sex']]
gss_table = round(gss_table.groupby(['sex']).mean(), 2)
gss_table = gss_table.rename({'income':'mean income', 'job_prestige':'mean job prestige index', 
                              'socioeconomic_index':'mean socioeconomic index', 'education':'mean years of education'},
                            axis=1).reset_index()
table = ff.create_table(gss_table)
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category')
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].cat.reorder_categories(['strongly agree',
                                                         'agree',
                                                         'disagree',
                                                         'strongly disagree'])
gss_clean['satjob'] = gss_clean['satjob'].astype('category')
gss_clean['satjob'] = gss_clean['satjob'].cat.reorder_categories(['very satisfied',
                                                         'mod. satisfied',
                                                         'a little dissat',
                                                         'very dissatisfied'])
gss_clean['relationship'] = gss_clean['relationship'].astype('category')
gss_clean['relationship'] = gss_clean['relationship'].cat.reorder_categories(['strongly agree',
                                                         'agree',
                                                         'disagree',
                                                         'strongly disagree'])
gss_clean['men_bettersuited'] = gss_clean['men_bettersuited'].astype('category')
gss_clean['men_bettersuited'] = gss_clean['men_bettersuited'].cat.reorder_categories(['agree',
                                                         'disagree'])
gss_clean['child_suffer'] = gss_clean['child_suffer'].astype('category')
gss_clean['child_suffer'] = gss_clean['child_suffer'].cat.reorder_categories(['strongly agree',
                                                         'agree',
                                                         'disagree',
                                                         'strongly disagree'])
gss_clean['men_overwork'] = gss_clean['men_overwork'].astype('category')
gss_clean['men_overwork'] = gss_clean['men_overwork'].cat.reorder_categories(['strongly agree',
                                                         'agree',
                                                         'neither agree nor disagree',
                                                         'disagree',
                                                         'strongly disagree'])
scat = px.scatter(gss_clean, x='job_prestige', y='income',
                color='sex',
                hover_data=['education', 'socioeconomic_index'],
                trendline='ols',
                labels={'job_prestige':'Occupational Prestige', 'income':'Income'})
boxes = pd.melt(gss_clean, id_vars=['sex'], value_vars=['income', 'job_prestige'])
fig1 = px.box(boxes.loc[boxes['variable']=='income'], x='value', y='sex', color='sex',
             labels={'value':'Income', 'sex':''})
fig1.update_layout(showlegend=False)
fig2 = px.box(boxes.loc[boxes['variable']=='job_prestige'], x='value', y='sex', color='sex',
             labels={'value':'Occupational Prestige', 'sex':''})
fig2.update_layout(showlegend=False)
gss6 = gss_clean[['income', 'sex', 'job_prestige']]
gss6['job_prestige'] = pd.cut(gss6.job_prestige, bins=6)
gss6 = gss6.dropna()
box_grid = px.box(gss6, x='income', y='sex', color='sex', facet_col='job_prestige', facet_col_wrap=2,
            labels={'income':'Income', 'sex':'Sex', 'job_prestige':'Occupational Prestige'},
            color_discrete_map = {'male':'blue', 'female':'red'})
box_grid.update_layout(showlegend=True)
cats = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']
groups = ['sex', 'region', 'education']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout  = html.Div(
    [
        html.H1('An Examination of the Gender Wage Gap, Using GSS Data'),
        
        dcc.Markdown(children=context),
        
        html.H2('Mean Occupational and Educational Statistics for Men and Women'),
        
        dcc.Graph(figure=table),
        
        html.H2('Agreement With the Statement: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family", by Sex'),
        
        html.Div([
            
            html.H3("category"),
            
            dcc.Dropdown(id='categories',
                         options=[{'label': i, 'value': i} for i in cats]),
            
            html.H3("groups"),
            
            dcc.Dropdown(id='groups',
                         options=[{'label': i, 'value': i} for i in groups])
            
        
        ], style={'width': '25%', 'float': 'left'}),
        
        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'}),
        
        html.H2('Occupational Prestige vs. Income, by Sex'),
        
        dcc.Graph(figure=scat),
        
        html.Div([
            html.H2('Distribution of Income, by Sex'),
            
            dcc.Graph(figure=fig1)
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            html.H2('Distribution of Occupational Prestige, by Sex'),
            
            dcc.Graph(figure=fig2)
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2('Income Distributions, by Sex and by Occupational Prestige'),
        
        dcc.Graph(figure=box_grid)
    

    
    ]
)

@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='categories',component_property="value"),
                   Input(component_id='group',component_property="value")])

def make_figure(categories, group):
    gss_bar = gss_clean.groupby([categories, group]).size()
    gss_bar = gss_bar.reset_index()
    gss_bar = gss_bar.rename({0:'count'}, axis=1)
    return px.bar(gss_bar, x=categories, y='count', color=group, 
       labels={category:'Level of Agreement'},
      barmode='group')


if __name__ == '__main__':
    app.run_server(debug=True)
