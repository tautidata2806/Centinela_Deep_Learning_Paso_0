"""Reproduce el recorte, la unión y el anexo A desde las dos fuentes oficiales.

Ejecutar desde la raíz: python scripts/preparar_datos.py
No descarga fotos: sus URL quedan en el CSV para descarga selectiva posterior.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
GLOBE = RAW / "globe_2024.csv.zip"
POWER = RAW / "power_2024_hourly.json"
LABELS = {"none": 0, "few": 0, "isolated": 0, "scattered": 0,
          "broken": 1, "overcast": 1}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    power = json.loads(POWER.read_text(encoding="utf-8"))
    params = power["properties"]["parameter"]
    rows = []
    raw_count = 0
    with ZipFile(GLOBE) as archive:
        name = next(n for n in archive.namelist() if n.endswith(".csv"))
        with archive.open(name) as source:
            reader = csv.DictReader(line.decode("utf-8-sig", "replace") for line in source)
            for r in reader:
                raw_count += 1
                try:
                    lat = float(r["Observation Latitude"])
                    lon = float(r["Observation Longitude"])
                except (ValueError, TypeError):
                    continue
                if not (28.5 <= lat < 28.75 and -81.75 <= lon < -81.5):
                    continue
                cover = r["Total Cloud Cover"].strip().lower()
                photo = r["Ground Image Up"].strip()
                if cover not in LABELS or not photo.startswith("https://data.globe.gov/"):
                    continue
                date = r["Measurement Date (UTC)"]
                hour = r["Measurement Time (UTC)"][:2]
                key = date.replace("-", "") + hour
                if key not in params["T2M"] or not 13 <= int(hour) <= 22:
                    continue
                # La serie de entrada termina una hora ANTES de la fotografía.
                prior = str(int(key) - 1) if hour != "00" else None
                if prior not in params["T2M"]:
                    continue
                rows.append({
                    "observation_id": r["Observation Id"],
                    "site_id": r["Site ID"],
                    "date_utc": date,
                    "hour_utc": hour,
                    "latitude": lat,
                    "longitude": lon,
                    "photo_url": photo,
                    "cloud_cover_original": cover,
                    "risk_binary": LABELS[cover],
                    "power_grid_lat": 28.625,
                    "power_grid_lon": -81.625,
                    "power_hour_utc": prior,
                    "power_t2m_prior_c": params["T2M"][prior],
                    "power_rh2m_prior_pct": params["RH2M"][prior],
                    "power_irradiance_prior_wh_m2": params["ALLSKY_SFC_SW_DWN"][prior],
                })
    columns = list(rows[0])
    with (OUT / "observaciones_unidas.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, columns)
        writer.writeheader()
        writer.writerows(rows)
    # Diez fechas distintas evitan una prueba inflada por fotos del mismo instante.
    seen = set()
    examples = []
    for row in rows:
        if row["date_utc"] not in seen:
            examples.append(row)
            seen.add(row["date_utc"])
        if len(examples) == 10:
            break
    with (OUT / "anexo_a_10_uniones.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, columns)
        writer.writeheader()
        writer.writerows(examples)
    stats = {
        "raw_globe_rows": raw_count,
        "joined_rows": len(rows),
        "unique_dates": len({r["date_utc"] for r in rows}),
        "unique_sites": len({r["site_id"] for r in rows}),
        "class_counts": dict(Counter(str(r["risk_binary"]) for r in rows)),
        "original_cover_counts": dict(Counter(r["cloud_cover_original"] for r in rows)),
        "missing_photo_in_joined_rows": sum(not r["photo_url"] for r in rows),
        "power_hours": len(params["T2M"]),
        "sha256": {GLOBE.name: sha256(GLOBE), POWER.name: sha256(POWER)},
    }
    (OUT / "verificacion.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
