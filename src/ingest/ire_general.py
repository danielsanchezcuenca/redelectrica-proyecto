import os, requests,json,argparse
from dotenv import load_dotenv
from src.utils.gcs import upload_json
from src.utils.dates import last_24h_window, now_tz, partition_str, timestamp_str

load_dotenv("config/.env")
BUCKET = os.getenv("GCS_BUCKET", "redelectrica-raw")
TZ = os.getenv("TZ", "Europe/Madrid")

BASE = "https://apidatos.ree.es/{lang}/datos/demanda/ire-general"

def fetch_ire (lang, start_date, end_date, time_trunc, geo_trunc, geo_limit, geo_ids):
    url= BASE.format(lang=lang)
    params = {
        "start_date":start_date,
        "end_date":end_date,
        "time_trunc":time_trunc,
        "geo_trunc":geo_trunc,
        "geo_limit":geo_limit,
        "geo_ids":geo_ids
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json(),params

def main():
    parser = argparse.ArgumentParser(description="Ingesta REE IRE General -> GCS")
    parser.add_argument("--lang", default="es",help="es|en")
    parser.add_argument("--start", required= True, help="YYYY-MM-DDTHH:MM")
    parser.add_argument("--end", required= True, help="YYYY-MM-DDTHH:MM")
    parser.add_argument("--time-trunc", default="month", choices=["hour","day","month","year"])
    parser.add_argument("--geo-trunc", default="electric_system")
    parser.add_argument("--geo-limit", default="peninsular")
    parser.add_argument("--geo-ids", default="8741")
    args = parser.parse_args()

    payload , used = fetch_ire(
        args.lang, args.start, args.end, args.time_trunc, args.geo_trunc, args.geo_limit, args.geo_ids
    )

     # Partición por la fecha de inicio (puedes cambiar a fin si te encaja mejor)

    part = args.start.split("T")[0]
    ts = timestamp_str(now_tz(TZ))

    # Carpeta descriptiva (incluye geo y time_trunc para diferenciar extracciones)

    path = (
        f"raw/ire_general/"
        ##f"geo={args.geo_limit}_{args.geo_ids}/"
        f"time_trunc={args.time_trunc}/"
        f"partition_date={part}/"
        f"ire_{ts}.json"
    )

    uri = upload_json(BUCKET, path, {"requests":used, "data" : payload})
    print("Subido", uri)

if __name__ == "__main__":
    main()