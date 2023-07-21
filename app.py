from operator import concat
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State  # pip install dash (version 2.0.0 or higher)
import matplotlib.pyplot as plt
import plotly.tools as tls
import psycopg2


app = Dash(__name__)

def query():
    PSQL_HOST = "static.99minutos.app"
    PSQL_PORT = "5432"
    PSQL_USER = "opschile"
    PSQL_PASS = "NDAhhH4sP67754"
    PSQL_DB   = "pr99minutoscom"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    sqlquery = "SELECT o.counter FROM logsorders lo LEFT JOIN orders o ON o.id = lo.orderid LEFT JOIN useraccounts ua ON ua.id = o.userid LEFT JOIN catdestinationadress ctd ON ctd.id = o.destionationadressid LEFT JOIN orderdetails od ON od.orderid = o.id LEFT JOIN catpickupadress ctpa ON ctpa.id=o.pickupadressid LEFT JOIN drivers d ON d.id=lo.driverid LEFT JOIN drivers di ON di.id=o.driverid  LEFT JOIN catclients c ON c.id=o.clientid WHERE lo.created BETWEEN '2023-07-20 00:00:00'AND'2023-07-20 23:59:59' AND ua.country ='CHL' AND lo.statusid IN ('3');"
    df_ptos =  pd.read_sql_query(sqlquery, conn)
    df_ptos["counter"] = df_ptos["counter"].astype(str)
    df_ptos = pd.DataFrame(df_ptos)
    return df_ptos


app.layout = html.Div([

    html.H1("Verificación de direcciones", style={'text-align': 'center'}),
    dcc.Store(id='signal'),
    dcc.Input(
        id = 'Input2',
        placeholder='Ingresa el Folio...',
        type='text',
        value=''),
    html.Button('Enviar', id='boton1'),
    html.Div(id='output_container', children=[]),
    html.Br(),
    ])


@app.callback(
    [Output(component_id='output_container', component_property='children')],
    [Input(component_id='boton1', component_property='n_clicks')])

def global_store(n_click):
    data = query()
    inducido = data.shape[0]
    container = "Cantidad de Folios Inducidos: {}".format(inducido)
    return [container]

if __name__ == '__main__':
    app.run_server(debug=True)