
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Cargar datos
df = pd.read_csv("https://raw.githubusercontent.com/german-viso/datasets/main/inmuebles_bogota.csv")

# Preprocesamiento
df = df[df["precio"].notnull() & df["area"].notnull()]
df["estrato"] = df["estrato"].fillna("Sin Dato")
df["precio_m2"] = df["precio"] / df["area"]

# Inicializar app Dash
app = dash.Dash(__name__)
app.title = "Análisis de Inmuebles en Bogotá"

# Layout de la app
app.layout = html.Div([
    html.H1("Análisis de Inmuebles por Estrato en Bogotá", style={"textAlign": "center"}),
    
    html.Label("Selecciona una ciudad:"),
    dcc.Dropdown(
        id="ciudad-dropdown",
        options=[{"label": ciudad, "value": ciudad} for ciudad in df["ciudad"].unique()],
        value="Bogotá D.C."
    ),

    dcc.Graph(id="grafico-pie"),
    html.Div(id="descripcion", style={"marginTop": "20px"})
])

# Callback para actualizar gráfico y descripción
@app.callback(
    [Output("grafico-pie", "figure"),
     Output("descripcion", "children")],
    [Input("ciudad-dropdown", "value")]
)
def actualizar_grafico(ciudad):
    df_filtrado = df[df["ciudad"] == ciudad]
    agrupado = df_filtrado.groupby("estrato").agg(
        cantidad=("estrato", "count"),
        promedio_precio_m2=("precio_m2", "mean")
    ).reset_index()

    agrupado["precio_m2_fmt"] = agrupado["promedio_precio_m2"].apply(lambda x: f"${x:,.0f}")

    fig = px.pie(
        agrupado,
        names="estrato",
        values="cantidad",
        title=f"Participación de inmuebles por estrato en {ciudad}",
        hole=0.4
    )

    descripcion = "En esta gráfica se puede observar la distribución de inmuebles por estrato y el precio promedio por m² para cada uno:\n\n"
    descripcion += "\n".join([f"- Estrato {row['estrato']}: {row['precio_m2_fmt']} por m² ({row['cantidad']} inmuebles)"
                              for _, row in agrupado.iterrows()])

    return fig, descripcion

# Ejecutar la app
if __name__ == "__main__":
    app.run_server(debug=True)
