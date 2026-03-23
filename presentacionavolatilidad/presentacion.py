import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

# =========================================================
# 1. DATOS DE EJEMPLO
# =========================================================
np.random.seed(42)

dates = pd.date_range("2024-01-01", periods=120, freq="D")

df_prices = pd.DataFrame({
    "Fecha": dates,
    "BTC": 42000 + np.cumsum(np.random.normal(0, 500, len(dates))),
    "ETH": 2200 + np.cumsum(np.random.normal(0, 40, len(dates))),
    "BNB": 300 + np.cumsum(np.random.normal(0, 8, len(dates)))
})

df_returns = df_prices.copy()
for col in ["BTC", "ETH", "BNB"]:
    df_returns[col] = np.log(df_prices[col]).diff()

df_returns = df_returns.dropna()

# Formato largo para algunos gráficos
df_prices_long = df_prices.melt(id_vars="Fecha", var_name="Activo", value_name="Precio")
df_returns_long = df_returns.melt(id_vars="Fecha", var_name="Activo", value_name="Retorno")

# =========================================================
# 2. GRÁFICOS INTERACTIVOS
# =========================================================

# Gráfico 1: precios en el tiempo
fig1 = px.line(
    df_prices_long,
    x="Fecha",
    y="Precio",
    color="Activo",
    title="Precios de mercado",
    markers=False
)
fig1.update_layout(
    template="plotly_dark",
    height=500,
    title_x=0.5
)

# Gráfico 2: distribución de retornos
fig2 = px.histogram(
    df_returns_long,
    x="Retorno",
    color="Activo",
    marginal="box",
    barmode="overlay",
    nbins=50,
    title="Distribución de retornos"
)
fig2.update_traces(opacity=0.65)
fig2.update_layout(
    template="plotly_dark",
    height=500,
    title_x=0.5
)

# Gráfico 3: volatilidad móvil
vol_df = pd.DataFrame({"Fecha": df_returns["Fecha"]})
window = 15
for col in ["BTC", "ETH", "BNB"]:
    vol_df[col] = df_returns[col].rolling(window).std()

vol_long = vol_df.dropna().melt(id_vars="Fecha", var_name="Activo", value_name="Volatilidad")

fig3 = px.line(
    vol_long,
    x="Fecha",
    y="Volatilidad",
    color="Activo",
    title=f"Volatilidad móvil ({window} días)"
)
fig3.update_layout(
    template="plotly_dark",
    height=500,
    title_x=0.5
)

# Gráfico 4: animación tipo burbujas
bubble_df = []
for i, d in enumerate(df_returns["Fecha"]):
    for asset in ["BTC", "ETH", "BNB"]:
        bubble_df.append({
            "Fecha": d,
            "Activo": asset,
            "Retorno": df_returns.loc[df_returns["Fecha"] == d, asset].values[0],
            "Volatilidad": vol_df.loc[vol_df["Fecha"] == d, asset].values[0] if d in vol_df["Fecha"].values else np.nan,
            "Tamaño": abs(df_returns.loc[df_returns["Fecha"] == d, asset].values[0]) * 5000 + 10
        })

bubble_df = pd.DataFrame(bubble_df).dropna()

fig4 = px.scatter(
    bubble_df,
    x="Retorno",
    y="Volatilidad",
    animation_frame=bubble_df["Fecha"].astype(str),
    animation_group="Activo",
    size="Tamaño",
    color="Activo",
    hover_name="Activo",
    range_x=[bubble_df["Retorno"].min()*1.2, bubble_df["Retorno"].max()*1.2],
    range_y=[0, bubble_df["Volatilidad"].max()*1.2],
    title="Dinámica de retorno y volatilidad"
)
fig4.update_layout(
    template="plotly_dark",
    height=550,
    title_x=0.5
)

# =========================================================
# 3. CONVERTIR LOS GRÁFICOS A BLOQUES HTML
# =========================================================
div1 = plot(fig1, include_plotlyjs=True, output_type="div")
div2 = plot(fig2, include_plotlyjs=False, output_type="div")
div3 = plot(fig3, include_plotlyjs=False, output_type="div")
div4 = plot(fig4, include_plotlyjs=False, output_type="div")

# =========================================================
# 4. ARMAR LA PRESENTACIÓN HTML
# =========================================================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Presentación Dinámica en HTML</title>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #0b0f19;
            color: white;
            overflow-x: hidden;
        }}
        .slide {{
            min-height: 100vh;
            padding: 40px 50px;
            box-sizing: border-box;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }}
        .title-slide {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}
        h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
        }}
        h2 {{
            font-size: 2rem;
            margin-bottom: 20px;
            color: #8ec5ff;
        }}
        p {{
            font-size: 1.15rem;
            max-width: 900px;
            line-height: 1.6;
        }}
        .chart-container {{
            margin-top: 20px;
            background: rgba(255,255,255,0.03);
            border-radius: 18px;
            padding: 15px;
        }}
        .nav {{
            position: fixed;
            top: 15px;
            right: 20px;
            z-index: 1000;
            background: rgba(0,0,0,0.45);
            padding: 10px 14px;
            border-radius: 12px;
            backdrop-filter: blur(8px);
        }}
        .nav a {{
            color: #8ec5ff;
            text-decoration: none;
            margin-left: 12px;
            font-size: 0.95rem;
        }}
        .nav a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>

<div class="nav">
    <a href="#slide1">Inicio</a>
    <a href="#slide2">Precios</a>
    <a href="#slide3">Retornos</a>
    <a href="#slide4">Volatilidad</a>
    <a href="#slide5">Animación</a>
</div>

<section class="slide title-slide" id="slide1">
    <h1>Presentación Dinámica</h1>
    <h2>Gráficos interactivos en HTML con Python</h2>
    <p>
        Esta presentación reúne varios gráficos dinámicos en un solo archivo HTML.
        Se puede navegar con scroll o usando el menú superior.
    </p>
</section>

<section class="slide" id="slide2">
    <h2>1. Evolución de precios</h2>
    <p>Comparación interactiva de los precios por activo.</p>
    <div class="chart-container">
        {div1}
    </div>
</section>

<section class="slide" id="slide3">
    <h2>2. Distribución de retornos</h2>
    <p>Histograma y boxplot para analizar dispersión y forma de los retornos.</p>
    <div class="chart-container">
        {div2}
    </div>
</section>

<section class="slide" id="slide4">
    <h2>3. Volatilidad móvil</h2>
    <p>La volatilidad rolling permite visualizar los cambios de incertidumbre en el tiempo.</p>
    <div class="chart-container">
        {div3}
    </div>
</section>

<section class="slide" id="slide5">
    <h2>4. Dinámica animada</h2>
    <p>Animación de retorno vs volatilidad para observar la evolución del mercado.</p>
    <div class="chart-container">
        {div4}
    </div>
</section>

</body>
</html>
"""

# =========================================================
# 5. GUARDAR ARCHIVO
# =========================================================
output_file = "presentacion_dinamica.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Archivo guardado como: {output_file}")