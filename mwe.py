############################################################################
# Bruno Vieira Ribeiro - Instituto Federal de Educação, Ciência e Tecnologia
# Setembro de 2021
############################################################################


## Imports necessários

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
import json


## Lendo dados em formato csv
final_df = pd.read_csv('dados_minimos.csv')
validadas = pd.read_csv('validadas.csv')


## Preparando lista de dicionários para dropdown das iniciativas
iniciativas_options = []
for ini in validadas['Iniciativa'].unique():
    my_dict = {}
    my_dict['label'] = str(ini)
    my_dict['value'] = str(ini)
    iniciativas_options.append(my_dict)
iniciativas_options = sorted(iniciativas_options, key = lambda k: k['label'])

## Funções de criar gráficos
def mapa_municipio(final_df, choice):
    '''
    Função que mapeia as iniciativas em seus respectivos pares (longitude,latitude).
    O argumento 'choice' (string) destaca em cor diferente as iniciativas que contém a string 'choice'.
    '''

    indice_escolha = final_df.index[final_df['Iniciativa'] == choice].tolist()

    seq_cores = [
        '' if (i in indice_escolha) else ' '
        for i in range(len(final_df))
    ]

    seq_sizes = [
        5 if (i in indice_escolha) else 1
        for i in range(len(final_df))
    ]

    fig = px.scatter_mapbox(
        final_df,
        lat="latitude",
        lon="longitude",
        zoom=3,
        color=seq_cores,
        color_discrete_sequence=['green', 'red'],
        size=seq_sizes,
        size_max=10,
        center={
                "lat": -15.46,
                "lon": -55.26
                },
        # mapbox_style="carto-positron",
        mapbox_style="open-street-map",
        hover_name='Iniciativa',
        hover_data={
            'latitude': False,
            'longitude': False,
            'Município': True,
            'Estado': True
        },
        width=650,
        height=600)

    fig.layout.update(showlegend=False)
    fig.update_traces(
        hovertemplate=
        '<b>%{hovertext}</b><br><br>Município=%{customdata[2]}<br>Estado=%{customdata[3]}<extra></extra>'
    )

    return fig

##########################################
########################################## INÍCIO DO APP
##########################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

## Corpo do layout do app
app.layout = html.Div([
    
    dbc.Row([
        dbc.Col([
            # Lista em dropdown das diferentes iniciativas cadastradas
            dcc.Dropdown(id='escolha-ini',
                                options = iniciativas_options,
                                style={'color': '#000000'},
                                value = 'Guia Gastronômico Do Distrito Federal',
                                placeholder = 'Busca por iniciativa...',
                                optionHeight = 60
                                ),
        ]),
        dbc.Col([
            # Espaço para plotar o mapa usando a função mapa_municipio()
            dcc.Graph(id='mapa-por-mun')
        ])
    ])
])


#################################### Início dos Callbacks (funções que fazem o link com elementos interativos)


####################
#################### Página dos Municípios
####################
@app.callback(
    Output("mapa-por-mun", "figure"),
    Input("escolha-ini", "value")
)
def plota_mapa_mun(ini):
    return mapa_municipio(final_df, ini)


####################################
if __name__ == '__main__':
    app.run_server()
