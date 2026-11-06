"""Descarga los dos archivos originales desde productores primarios.

Uso: python scripts/descargar_fuentes.py
No sobrescribe archivos presentes. Después: python scripts/preparar_datos.py
"""
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SOURCES = {
    "globe_2024.csv.zip": "https://zenodo.org/records/18763550/files/2024_GLOBE_AnnualCloudObs_2026-01-05_v3-4.csv.zip?download=1",
    "power_2024_hourly.json": "https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=ALLSKY_SFC_SW_DWN,T2M,RH2M&community=RE&longitude=-81.625&latitude=28.625&start=20240101&end=20241231&time-standard=UTC&format=JSON",
}


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        target = RAW / name
        if target.exists() and target.stat().st_size:
            print(f"Ya existe: {target}")
            continue
        req = Request(url, headers={"User-Agent": "CentinelaAcademico/1.0"})
        with urlopen(req, timeout=120) as response, target.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        print(f"Descargado: {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
