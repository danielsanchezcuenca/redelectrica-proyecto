# Proyecto Red Eléctrica (Ingesta en GCP)

Este proyecto ingiere datos abiertos de **Red Eléctrica (REData API)** y los sube a **Google Cloud Storage (GCS)** en formato JSON.  

La estructura de carpetas está organizada en `src/ingest/` con un script por cada widget principal de la API:

- `ire_general.py` → Índice de Red Eléctrica (demanda).
- `balance.py` → Balance eléctrico.
- `estructura.py` → Estructura de generación.

Los archivos se almacenan en el bucket con prefijos jerárquicos (`raw/...`) siguiendo buenas prácticas de **data lake**.  

---

## 🔧 Requisitos

- Python 3.12+  
- Entorno virtual (`.venv`) activado  
- Dependencias en `requirements.txt`:
  ```txt
  requests
  python-dotenv
  python-dateutil
  google-cloud-storage


## Configuración del env:

GCP_PROJECT_ID=redelectrica-470416
GCS_BUCKET=redelectrica-raw
TZ=Europe/Madrid

## Autentiación GCP:
gcloud auth application-default login

# Ejecución de scripts

Los scripts deben ejecutarse desde la carpeta raíz del proyecto usando el flag -m para que funcionen los imports:

1. IRE General (Demanda)

	•	Península:
  python3 -m src.ingest.ire_general \
  --lang es \
  --start 2018-01-01T00:00 \
  --end   2018-12-31T23:59 \
  --time-trunc month \
  --geo-trunc electric_system \
  --geo-limit peninsular \
  --geo-ids 8741

	•	Nacional (toda España):
  python3 -m src.ingest.ire_general \
    --lang es \
    --start 2018-01-01T00:00 \
    --end   2018-12-31T23:59 \
    --time-trunc month

2. Balance Eléctrico

⚠️ Este endpoint no admite parámetros geo (si los añades da error).

python3 -m src.ingest.balance \
  --lang es \
  --start 2020-01-01T00:00 \
  --end   2020-12-31T23:59 \
  --time-trunc month

  3. Estructura de Generación

⚠️ Importante: solo funciona con time_trunc=year (no acepta mes o día).
	•	Nacional (no pasar geo params):
  python3 -m src.ingest.estructura \
  --lang es \
  --start 2020-01-01T00:00 \
  --end   2020-12-31T23:59 \
  --time-trunc year

  	•	Por CCAA (ejemplo Castilla-La Mancha, id=7):

    python3 -m src.ingest.estructura \
  --lang es \
  --start 2020-01-01T00:00 \
  --end   2020-12-31T23:59 \
  --time-trunc year \
  --geo-trunc electric_system \
  --geo-limit ccaa \
  --geo-ids 7


  📊 Diferencias clave entre endpoints
	•	IRE General
	•	Acepta geo_trunc=electric_system con geo_limit=peninsular (geo_ids=8741).
	•	Sin geo → devuelve nacional.
	•	Con ccaa → puedes pedir por comunidad.
	•	Balance Eléctrico
	•	Solo nacional, sin parámetros geo.
	•	Estructura Generación
	•	Nacional si no pasas geo.
	•	Si pasas geo, debes incluir geo_trunc + geo_limit + geo_ids (ej. ccaa).
	•	No admite peninsular.
