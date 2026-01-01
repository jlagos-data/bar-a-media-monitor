# Barça Media Reputation Monitor


Este proyecto es una herramienta de **inteligencia de datos** diseñada para monitorizar y analizar la reputación del **FC Barcelona** en los medios de comunicación internacionales en cada 3 dias.

---

### Acceso Directo
Puedes ver el dashboard en tiempo real aquí: [barca-media-monitor.streamlit.app](https://bar-a-media-monitor-3cwq5qrsyviqe4hpftuvny.streamlit.app)

## Funcionalidades

* **Extracción Automatizada:** Obtiene las últimas noticias utilizando la API de NewsAPI.

* **Análisis de Sentimiento:** Clasifica automáticamente las noticias en *Positivas*, *Negativas* o *Neutras* mediante procesamiento de lenguaje natural (NLP) con **TextBlob**.

* **Dashboard Interactivo:** Visualización de métricas clave, alertas de crisis y distribución de fuentes a través de **Streamlit**.

* **Alertas de Reputación:** Sistema visual que detecta volúmenes críticos de noticias negativas.


## Stack Tecnológico

* **Lenguaje:** Python 3.12

* **Base de Datos:** SQLite (SQLAlchemy)

* **Librerías Principales:** Pandas, Streamlit, Plotly, TextBlob, Requests.

* **API:** NewsAPI.

  
## Estructura del Proyecto

* `extractor.py`: Script encargado de la extracción, procesamiento y carga de datos (ETL).

* `dashboard.py`: Aplicación web interactiva para visualizar los datos.

* `reputation.db`: Base de datos local con el histórico de noticias.

* `.env`: Archivo de configuración para claves de API (no incluido en el repo).

  

## Instalación y Uso

1. **Clonar el repositorio:**

```bash

git clone [https://github.com/jlagos-data/barca-media-monitor.git](https://github.com/jlagos-data/barca-media-monitor.git)

cd barca-media-monitor

```

  
2. **Instalar dependencias:**

```bash

pip install -r requirements.txt

```

  
3. **Configurar credenciales:**

Crea un archivo `.env` en la raíz y añade tu API Key:

```env

NEWS_API_KEY=tu_clave_aqui

```

  
4. **Ejecutar el Extractor (para actualizar datos):**

```bash

python extractor.py

```


5. **Lanzar el Dashboard:**

```bash

streamlit run dashboard.py

```
