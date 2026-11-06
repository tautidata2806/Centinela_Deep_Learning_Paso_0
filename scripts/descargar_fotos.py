"""Descarga fotos desde las URL oficiales del CSV curado.

python scripts/descargar_fotos.py --limit 10
python scripts/descargar_fotos.py --all   # después de aprobar la propuesta
"""
import argparse
import csv
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
PHOTOS = ROOT / "data" / "raw" / "photos"


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--limit", type=int)
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()
    source = DATA / ("observaciones_unidas.csv" if args.all else "anexo_a_10_uniones.csv")
    PHOTOS.mkdir(parents=True, exist_ok=True)
    with source.open(encoding="utf-8", newline="") as f:
        records = list(csv.DictReader(f))
    if args.limit is not None:
        records = records[:args.limit]
    def download(row):
        dest = PHOTOS / f"{row['observation_id']}.jpg"
        if dest.exists() and dest.stat().st_size > 0:
            return True, f"ya existe {dest.name}"
        try:
            req = urllib.request.Request(row["photo_url"], headers={"User-Agent": "CentinelaAcademico/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                dest.write_bytes(response.read())
            return True, f"{dest.name} {dest.stat().st_size} bytes"
        except Exception as exc:
            dest.unlink(missing_ok=True)
            return False, f"{dest.name}: {exc}"

    ok = 0
    failures = []
    with ThreadPoolExecutor(max_workers=6 if args.all else 3) as pool:
        futures = {pool.submit(download, row): row for row in records}
        for i, future in enumerate(as_completed(futures), 1):
            success, message = future.result()
            ok += success
            if not success:
                failures.append(message)
                print("ERROR", message, flush=True)
            elif i % 100 == 0 or i == len(records):
                print(f"{i}/{len(records)} procesadas; {ok} disponibles", flush=True)
    if failures:
        (PHOTOS / "fallos_descarga.txt").write_text("\n".join(failures), encoding="utf-8")
    print(f"Resultado: {ok}/{len(records)} fotos disponibles; {len(failures)} fallos")


if __name__ == "__main__":
    main()
