import pandas as pd
import plotly.express as px
import dash
import os
from dash import html, dcc
from dash.dependencies import Input, Output
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('dashboard/datos_ciudades.csv')

# Preprocesamiento general
df['precio_millones'] = (df['precio'] / 1_000_000).round(2)
df['precio_millones_str'] = df['precio_millones'].apply(lambda x: f"${x:,.1f}M")
df['info_hover'] = (
    "🏘️ " + df['ubicacion_asociada'].astype(str) +
    "<br>💲 " + df['precio_millones_str'] +
    "<br>🛏️ " + df['habitaciones'].astype(str) +
    "<br>💧 " + df['baños'].astype(str)
)
df['precio_texto'] = df['precio_millones'].apply(lambda x: f"{int(x):,}".replace(",", ".") + " millones")
df['precio_m2'] = df['precio'] / df['area m²']
lotes_df = df[df['tipo_inmueble'].str.lower() == 'lote'].copy()

# Crear app principal
app = dash.Dash(__name__)
app.title = "Dashboard Inmobiliario"

# Layout principal con Tabs
app.layout = html.Div([ 
    html.H1("Dashboard Inmobiliario – Boyacá", style={'textAlign': 'center'}),
    dcc.Tabs(id='tabs', value='tab-mapa', children=[ 
        dcc.Tab(label='Mapa de Precios', value='tab-mapa'),
        dcc.Tab(label='Precio vs Área', value='tab-barra'),
        dcc.Tab(label='Lotes por Ciudad', value='tab-lotes'),
        dcc.Tab(label='Precio Promedio por m²', value='tab-precio-m2'),
        dcc.Tab(label='Precio Promedio por Tipo de Inmueble', value='tab-precio-tipo'),
        dcc.Tab(label='Inmuebles por Ciudad', value='tab-ciudad')
    ]),
    html.Div(id='contenido-tab')
])

# Callbacks para Tabs
@app.callback(Output('contenido-tab', 'children'), Input('tabs', 'value'))
def render_tab(tab):
    if tab == 'tab-mapa':
        return html.Div([ 
            html.Label("Ciudad:"),
            dcc.Dropdown(id='filtro-ciudad', options=[{'label': c, 'value': c} for c in sorted(df['Ciudad'].dropna().unique())], value=sorted(df['Ciudad'].dropna().unique())[0]),
            html.Label("Tipo de Inmueble:"),
            dcc.Dropdown(id='filtro-tipo', options=[{'label': t, 'value': t} for t in sorted(df['tipo_inmueble'].dropna().unique())], value=None, placeholder="Todos"),
            html.Label("Estrato:"),
            dcc.Dropdown(id='filtro-estrato', options=[{'label': str(e), 'value': e} for e in sorted(df['estrato'].dropna().unique())], value=None, placeholder="Todos"),
            dcc.Graph(id='mapa-precios')
        ], style={'width': '60%', 'margin': 'auto'})

    elif tab == 'tab-barra':
        return html.Div([ 
            html.Label("Ciudad:"),
            dcc.Dropdown(id='ciudad-barra', options=[{'label': c, 'value': c} for c in sorted(df['Ciudad'].dropna().unique())], value=sorted(df['Ciudad'].dropna().unique())[0]),
            html.Label("Estrato:"),
            dcc.Dropdown(id='estrato-barra', options=[{'label': str(e), 'value': e} for e in sorted(df['estrato'].dropna().unique())], value=None, placeholder="Todos"),
            dcc.Graph(id='grafico-precio-area')
        ], style={'width': '60%', 'margin': 'auto'})

    elif tab == 'tab-lotes':
        return html.Div([ 
            html.Label("Ciudad:"),
            dcc.Dropdown(id='ciudad-lotes', options=[{'label': c, 'value': c} for c in sorted(lotes_df['Ciudad'].dropna().unique())], value=sorted(lotes_df['Ciudad'].dropna().unique())[0]),
            dcc.Graph(id='mapa-lotes')
        ], style={'width': '60%', 'margin': 'auto'})

    elif tab == 'tab-precio-m2':
        return html.Div([ 
            html.Label("Ciudad:"),
            dcc.Dropdown(id='ciudad-torta', options=[{'label': c, 'value': c} for c in sorted(df['Ciudad'].dropna().unique())], value=sorted(df['Ciudad'].dropna().unique())[0]),
            dcc.Graph(id='grafico-precio-m2')
        ], style={'width': '60%', 'margin': 'auto'})

    elif tab == 'tab-precio-tipo':
        return html.Div([
            html.Label("Ciudad:"),
            dcc.Dropdown(
            id='ciudad-precio-tipo',
            options=[{'label': c, 'value': c} for c in sorted(df['Ciudad'].dropna().unique())], value=sorted(df['Ciudad'].dropna().unique())[0]), dcc.Graph(id='grafico-precio-tipo')
        ], style={'width': '60%', 'margin': 'auto'})

    elif tab == 'tab-ciudad':
        return html.Div([
            dcc.Graph(id='grafico-inmuebles-ciudad')
        ], style={'width': '80%', 'margin': 'auto'})
# Callback Mapa Precios
@app.callback(Output('mapa-precios', 'figure'),
              Input('filtro-ciudad', 'value'),
              Input('filtro-tipo', 'value'),
              Input('filtro-estrato', 'value'))
def actualizar_mapa(ciudad, tipo_inmueble, estrato):
    df_f = df[df['Ciudad'] == ciudad]
    if tipo_inmueble: df_f = df_f[df_f['tipo_inmueble'] == tipo_inmueble]
    if estrato: df_f = df_f[df_f['estrato'] == estrato]
    fig = px.scatter_mapbox(
        df_f, lat='latitud', lon='longitud', color='precio_millones', size='precio_millones',
        hover_name='info_hover', mapbox_style="open-street-map", zoom=12,
        color_continuous_scale='Plasma', title="Mapa de precios"
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# Callback Gráfico Barra Precio vs Área
@app.callback(Output('grafico-precio-area', 'figure'),
              Input('ciudad-barra', 'value'),
              Input('estrato-barra', 'value'))
def actualizar_barra(ciudad, estrato):
    df_f = df[df['Ciudad'] == ciudad]
    if estrato: df_f = df_f[df_f['estrato'] == estrato]
    df_f = df_f.sort_values(by='precio', ascending=False).head(30)
    fig = px.bar(df_f, x='area m²', y='precio_millones', color='estado_inmueble',
                 hover_name='ubicacion_asociada', labels={'area m²': 'Área (m²)', 'precio_millones': 'Precio (Millones COP)'},
                 title="Precio vs Área en m²")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# Callback Mapa Lotes
@app.callback(Output('mapa-lotes', 'figure'),
              Input('ciudad-lotes', 'value'))
def actualizar_lotes(ciudad):
    df_f = lotes_df[lotes_df['Ciudad'] == ciudad]
    fig = px.scatter_mapbox(
        df_f, lat='latitud', lon='longitud', size='precio_millones', color='precio_millones',
        hover_name='ubicacion_asociada',
        mapbox_style="open-street-map", zoom=12,
        color_continuous_scale='Viridis',
        title=f"Lotes en {ciudad}"
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# Callback Gráfico Precio Promedio por m²
@app.callback(Output('grafico-precio-m2', 'figure'),
              Input('ciudad-torta', 'value'))
def actualizar_precio_m2(ciudad):
    df_f = df[df['Ciudad'] == ciudad]
    df_mean = df_f.groupby('estrato')['precio_m2'].mean().reset_index()
    fig = px.pie(df_mean, names='estrato', values='precio_m2', title=f"Precio promedio por m² en {ciudad}")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# Callback Precio Promedio por Tipo de Inmueble
@app.callback(Output('grafico-precio-tipo', 'figure'),
              Input('ciudad-torta', 'value'))
def actualizar_precio_tipo(ciudad):
    avg_price_by_type = df.groupby('tipo_inmueble')['precio_millones'].mean().reset_index()
    fig = px.bar(avg_price_by_type, x='tipo_inmueble', y='precio_millones', title="Precio Promedio por Tipo de Inmueble")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# Callback Inmuebles por Ciudad
@app.callback(Output('grafico-inmuebles-ciudad', 'figure'),
              Input('ciudad-torta', 'value'))
def actualizar_inmuebles_ciudad(ciudad):
    df_f = df[df['Ciudad'] == ciudad]
    fig = px.bar(df_f['Ciudad'].value_counts().reset_index(), x='index', y='Ciudad', title="Cantidad de Inmuebles por Ciudad")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

# Ejecutar
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Usa el puerto de la variable de entorno o 10000 por defecto
    app.run(host='0.0.0.0', port=port, debug=True)
