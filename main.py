import streamlit as st
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "contratos de café por departamento",
    "Aptitud del Suelo",
    "exportaciones",
    "Predicción de Demanda",
    "Calidad del Café",
    "Dashboard producción-calidad"
])


with tab1:


    # Código del iframe
    iframe_code = '''
    <iframe allow="geolocation" src="https://www.datos.gov.co/dataset/Caf-pyme/xey2-7hrp/embed?width=800&height=600" width="800" height="600" style="border:0; padding: 0; margin: 0;"></iframe>
    '''

    # Insertar el iframe en Streamlit
    components.html(iframe_code, height=600)



with tab2:
    # Título de la aplicación
    st.title("Mapa de Aptitud del Suelo para Café 'Coffea arabica'")

    # Incrustar el mapa en un iframe
    url2 = "https://www.arcgis.com/apps/mapviewer/index.html?url=https://geoservicios.upra.gov.co/arcgis/rest/services/aptitud_uso_suelo/Aptitud_Cafe_Jul2022/MapServer&source=sd"

    components.iframe(url2, width=1000, height=1300, scrolling=False)

with tab3:


    # Ruta del archivo Excel
    file_path = "exportaciones_1.xlsx"
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file_path)

        # Configuración de página
        st.title("Análisis de Datos por Países")
        st.header("Filtros")

        # Filtros de selección
        selected_years = st.multiselect(
            "Selecciona los años para analizar:",
            options=df.columns[1:],  # Excluir la columna 'PAISES'
            default=df.columns[1:],  # Seleccionar todos los años por defecto
        )

        selected_countries = st.multiselect(
            "Selecciona los países para incluir:",
            options=df["PAISES"].unique(),
            default=df["PAISES"].unique(),
        )

        # Filtrar DataFrame
        filtered_df = df[df["PAISES"].isin(selected_countries)][["PAISES"] + selected_years]

        # Mostrar tabla de datos filtrados
        st.header("Datos Filtrados")
        st.dataframe(filtered_df)

        # Gráfica de barras horizontal
        st.header("Comparación de Países")
        selected_metric = st.selectbox("Selecciona el año para graficar:", options=selected_years)

        if selected_metric:
            plt.figure(figsize=(10, 8))
            plt.barh(filtered_df["PAISES"], filtered_df[selected_metric], color='skyblue')
            plt.xlabel(f"Valor ({selected_metric})")
            plt.ylabel("Países")
            plt.title(f"Distribución por Países - Año {selected_metric}")
            plt.tight_layout()  # Asegura que los textos no se corten
            st.pyplot(plt)

        # Análisis de tendencias
        st.header("Tendencia por País")
        trend_country = st.selectbox("Selecciona un país para analizar la tendencia:", options=filtered_df["PAISES"])

        if trend_country:
            country_data = filtered_df[filtered_df["PAISES"] == trend_country].drop("PAISES", axis=1).T
            country_data.columns = ["Valores"]
            plt.figure(figsize=(10, 6))
            plt.plot(country_data, marker='o')
            plt.xlabel("Años")
            plt.ylabel("Valor")
            plt.title(f"Tendencia de {trend_country}")
            st.pyplot(plt)

        # Resumen
        st.header("Resumen")
        st.write(
            f"Se han seleccionado **{len(selected_countries)} países** y **{len(selected_years)} años** para el análisis."
        )
    except FileNotFoundError:
        st.error(f"El archivo en la ruta especificada '{file_path}' no se encontró. Verifica la ruta.")



    # ======= 1. Función para cargar el dataset =======
    @st.cache_data
    def load_data():
        # Simulación de un dataset de café
        data = {
            "Región": ["Antioquia", "Huila", "Caldas", "Tolima", "Cauca"],
            "Calidad": [4, 3.5, 4.2, 4.0, 3.8],
            "Altitud_msnm": [1500, 1700, 1600, 1800, 1750],
            "Producción_kg": [1000, 1200, 1100, 1300, 1250],
        }
        return pd.DataFrame(data)


    df = load_data()

    # ======= 2. Diccionario de coordenadas =======
    coordenadas = {
        "Antioquia": {"lat": 6.25184, "lon": -75.56359},
        "Huila": {"lat": 2.53594, "lon": -75.52767},
        "Caldas": {"lat": 5.026, "lon": -75.476},
        "Tolima": {"lat": 4.43889, "lon": -75.23222},
        "Cauca": {"lat": 2.44555, "lon": -76.61474},
    }
    df["lat"] = df["Región"].map(lambda x: coordenadas.get(x, {"lat": None})["lat"])
    df["lon"] = df["Región"].map(lambda x: coordenadas.get(x, {"lon": None})["lon"])


    # ======= 3. Función para cargar el modelo de predicción =======
    @st.cache_resource
    def load_model():
        with open("model.pkl", "rb") as file:
            return pickle.load(file)


    model = load_model()

with tab4:
    def render_home():
        st.title("🌟 Bienvenido al Sistema de Predicción y Calidad del Café 🌟")
        st.write("Explora la predicción de demanda y calidad del café con nuestra aplicación interactiva.")

        # Predicción de demanda
        st.header("📈 Predicción de Demanda")
        precio = st.number_input("Precio del Café (USD por libra):", min_value=0.5, max_value=5.0, step=0.1)
        calidad = st.slider("Calidad Promedio (1-5):", min_value=1, max_value=5)
        temperatura = st.number_input("Temperatura Media (°C):", min_value=10.0, max_value=40.0, step=0.5)
        lote = st.number_input("Tamaño del lote (kg):", min_value=1, max_value=1000, step=10)

        if st.button("Predecir Demanda"):
            demanda_predicha = model.predict([[precio, calidad, temperatura]])[0] * lote
            st.success(f"La demanda esperada para el lote de {lote} kg es: {int(demanda_predicha)} unidades.")
    render_home()


with tab5:


    def render_quality():
        st.title("Calidad del Café Histórico")
        st.write("Explora los datos históricos de calidad del café por región y características.")

        # Mapa interactivo
        st.subheader("Mapa Interactivo: Calidad del Café por Región")
        fig = px.scatter_geo(
            df,
            lat="lat",
            lon="lon",
            text="Región",
            size="Calidad",
            color="Calidad",
            hover_name="Región",
            projection="natural earth",
            title="Mapa de Calidad por Región",
        )
        st.plotly_chart(fig)

        # Gráfico de barras
        st.subheader("Comparación de Calidad por Región")
        fig_bar = px.bar(
            df,
            x="Región",
            y="Calidad",
            title="Calidad Promedio por Región",
            labels={"Calidad": "Calidad Promedio", "Región": "Región"},
            color="Calidad",
        )
        st.plotly_chart(fig_bar)

        # Línea de tiempo
        st.subheader("Producción y Calidad")
        df_timeline = pd.DataFrame(
            {
                "Fecha": pd.date_range(start="2023-01-01", periods=12, freq="M"),
                "Producción_kg": [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550],
                "Calidad": [4, 4.1, 4.2, 4.3, 4.0, 4.1, 4.2, 4.1, 4.3, 4.4, 4.2, 4.3],
            }
        )
        fig_timeline = px.line(
            df_timeline,
            x="Fecha",
            y=["Producción_kg", "Calidad"],
            title="Producción y Calidad del Café a lo Largo del Tiempo",
            labels={"value": "Valor", "Fecha": "Fecha", "variable": "Indicador"},
        )
        st.plotly_chart(fig_timeline)

    render_quality()

with tab6:
    st.title("📊 Dashboard General")

    # Métricas
    st.metric("Demanda Promedio (Últimos 12 Meses)", "273 unidades")
    st.metric("Precio Promedio del Café", "$1.15 USD")

    # Crear datos ficticios para el gráfico
    df_dashboard = pd.DataFrame(
        {
            "Mes": pd.date_range(start="2023-01-01", periods=12, freq="M"),
            "Producción_kg": [1000, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500, 1550, 1600],
            "Calidad": [4, 4.1, 4.2, 4.3, 4.0, 4.1, 4.2, 4.1, 4.3, 4.4, 4.2, 4.3],
        }
    )

    # Gráfico de progreso
    fig_dashboard = px.line(
        df_dashboard,
        x="Mes",
        y=["Producción_kg", "Calidad"],
        title="Progresión de Producción y Calidad",
        labels={"value": "Valor", "Mes": "Mes", "variable": "Indicador"}
    )
    st.plotly_chart(fig_dashboard)




