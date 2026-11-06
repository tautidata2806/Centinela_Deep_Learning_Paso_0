"""Comprueba todas las fotos esperadas y genera un manifiesto SHA-256.

Uso: python scripts/verificar_fotos.py
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "processed" / "observaciones_unidas.csv"
PHOTOS = ROOT / "data" / "raw" / "photos"
OUT = ROOT / "data" / "processed"


def main() -> None:
    with CSV.open(encoding="utf-8", newline="") as f:
        records = list(csv.DictReader(f))
    manifest = []
    invalid = []
    for row in records:
        path = PHOTOS / f"{row['observation_id']}.jpg"
        if not path.is_file():
            invalid.append(f"falta {path.name}")
            continue
        data = path.read_bytes()
        if not (data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9")):
            invalid.append(f"JPEG inválido {path.name}")
            continue
        manifest.append({"observation_id": row["observation_id"],
                         "file": path.name, "bytes": len(data),
                         "sha256": hashlib.sha256(data).hexdigest(),
                         "source_url": row["photo_url"]})
    with (OUT / "manifiesto_fotos.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, manifest[0].keys())
        writer.writeheader()
        writer.writerows(manifest)
    summary = {"expected": len(records), "valid": len(manifest),
               "invalid": invalid, "total_bytes": sum(r["bytes"] for r in manifest)}
    (OUT / "verificacion_fotos.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if invalid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
