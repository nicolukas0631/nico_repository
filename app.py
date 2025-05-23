import pandas as pd
import numpy as np  
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# leer los datos
vehicle_df = pd.read_csv('vehicles_us.csv') 
# Preparar los datos
vehicle_df.fillna({'model_year': 2025}, inplace=True)
vehicle_df['model_year'] = vehicle_df['model_year'].astype(int)

vehicle_df.fillna({'cylinders': 0}, inplace=True)
vehicle_df['cylinders'] = vehicle_df['cylinders'].astype(int)

vehicle_df.fillna({'odometer': -1}, inplace=True)
vehicle_df.fillna({'paint_color': 'unknown'}, inplace=True)

vehicle_df.fillna({'is_4wd': 0}, inplace=True)
vehicle_df.loc[vehicle_df['is_4wd'] == 1, 'is_4wd'] = True
vehicle_df.loc[vehicle_df['is_4wd'] == 0, 'is_4wd'] = False
vehicle_df['is_4wd'] = vehicle_df['is_4wd'].astype(bool)

duplicados = vehicle_df[vehicle_df.duplicated(subset=['price', 'model_year', 'model', 'condition', 'odometer', 'fuel', 'transmission', 'paint_color'],keep=False)]
df_drop_dupli = vehicle_df.drop_duplicates(subset=['price', 'model_year', 'model', 'condition', 'odometer', 'fuel', 'transmission', 'paint_color'],keep='first')
duplicados = duplicados.sort_values(by=['model_year', 'model', 'condition', 'odometer', 'fuel', 'transmission', 'paint_color', 'price', 'date_posted'])

# Crear la aplicación Streamlit
st.set_page_config(page_title="Análisis de datos de SaCar.com", page_icon=":car:", layout="wide")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title("Análisis de datos de SaCar.com")


with st.container():
    st.subheader("Descripción de la aplicación")
    st.markdown("""
Bienvenido a la aplicación interactiva de análisis de datos de **SaCar.com**.

Esta herramienta te permite explorar y visualizar información sobre anuncios de venta de vehículos publicados entre 2018 y 2019 en la plataforma ficticia SaCar.com.

El conjunto de datos incluye información sobre el año del modelo, el kilometraje, el color de la pintura y el número de cilindros de los vehículos, entre otros.
Puedes utilizar esta aplicación para analizar y visualizar estos datos de manera interactiva.
""")
    st.subheader("Visualización de datos")
    st.dataframe(vehicle_df)
    st.write("Nota: Los valores nulos han sido reemplazados por valores predeterminados. Por ejemplo, el año del modelo se ha establecido en 2025, el kilometraje en -1., el color de la pintura en 'desconocido' y el numero de cilindros en 0.") # mensaje informativo

co1, co2, co3 = st.columns([1, 2, 1])
with co2:
    st.subheader("Elige una opción para visualizar algunos datos")
    st.write("Puedes elegir entre un histograma, un gráfico de dispersión o un gráfico de líneas.")
    st.write("  ")

colu1, colu2, colu3 = st.columns([2, 2, 1])
with colu1:
    hist_button = st.button('Construir histograma', key='hist1') 
with colu2:
    scat_button = st.button('Construir un grafico de dispersión', key='hist2') 
with colu3:
    line_button = st.button('Construir grafico de lineas', key='hist3') 



# Grafica de dispersión
if scat_button:

    price_per_odometer_mean = vehicle_df[vehicle_df['odometer'] >= 0].groupby('odometer')['price'].mean().reset_index()
    price_per_odometer_mean = price_per_odometer_mean.sort_values(by='price', ascending=False)

    fig = px.scatter(
        price_per_odometer_mean,
        x='odometer',
        y='price',
        title='Correlación entre kilometraje y precio medio',
        labels={'odometer': 'Kilometraje', 'price': 'Precio medio'},
        color_discrete_sequence=["#1F2DEA"]
)
    fig.update_yaxes(title_text='Precio medio')
    st.plotly_chart(fig, use_container_width=True)

if hist_button: 
    fig = px.histogram(
        vehicle_df, x="odometer",
        title="Histograma del kilometraje de los vehículos",
        labels={"odometer": "Kilometraje"},
        color_discrete_sequence=["#1F2DEA"],
         # marginal="box",  BUEN USO
                    )
    st.plotly_chart(fig, use_container_width=True)
    st.write("Nota: Los valores nulos han sido reemplazados por -1.")

if line_button:
    type_per_days_listed = df_drop_dupli.groupby('days_listed')['type'].value_counts().unstack()
    fig = px.line(
        type_per_days_listed,
        x=type_per_days_listed.index,
        y=type_per_days_listed.columns,
        title='Tipo de vehículo por días listados',
        labels={'days_listed': 'Días listados', 'value': 'Cantidad'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_yaxes(title_text='Cantidad de vehículos')
    st.plotly_chart(fig, use_container_width=True)
