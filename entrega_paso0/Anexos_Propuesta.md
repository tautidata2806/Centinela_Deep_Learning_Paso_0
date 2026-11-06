# Anexos de la Propuesta de Datos

## A. Prueba de acoplamiento

La tabla completa, con URL de foto, coordenadas y valores POWER, está en [`data/processed/anexo_a_10_uniones.csv`](data/processed/anexo_a_10_uniones.csv). Son diez fechas diferentes, no diez copias de la misma hora. Los diez archivos JPG correspondientes se descargaron en `data/raw/photos/`. El código que produjo la unión es `scripts/preparar_datos.py`.

| Fecha UTC | ID de foto GLOBE | Nubosidad | Hora previa POWER | Temperatura °C | Humedad % |
|---|---|---|---|---:|---:|
| 2024-01-03 | 116-179641-117017173-202401031731 | broken | 2024-01-03 16:00 | 15,84 | 70,42 |
| 2024-01-07 | 116-344567-113325769-202401072231 | none | 2024-01-07 21:00 | 16,27 | 63,89 |
| 2024-01-09 | 116-334639-113325769-202401092102 | none | 2024-01-09 20:00 | 23,87 | 81,35 |
| 2024-01-10 | 116-179641-117017173-202401101731 | isolated | 2024-01-10 16:00 | 14,66 | 55,71 |
| 2024-01-19 | 116-179641-117317207-202401191817 | overcast | 2024-01-19 17:00 | 21,56 | 80,56 |
| 2024-01-22 | 116-179641-117017271-202401221359 | overcast | 2024-01-22 12:00 | 10,79 | 90,05 |
| 2024-01-23 | 116-179641-117309094-202401231831 | overcast | 2024-01-23 17:00 | 22,70 | 68,41 |
| 2024-01-24 | 116-179641-65303359-202401242012 | scattered | 2024-01-24 19:00 | 25,91 | 68,94 |
| 2024-01-26 | 116-181179-113319793-202401261902 | none | 2024-01-26 18:00 | 25,24 | 74,22 |
| 2024-01-29 | 116-344567-113325769-202401292255 | none | 2024-01-29 21:00 | 15,70 | 55,71 |

**Regla:** foto tomada en una celda de 0,25° alrededor de (28,625; -81,625). Se une con la hora UTC inmediatamente anterior de la serie POWER del centro de esa celda. Las observaciones no son co-registros exactos de parcela; el valor POWER es común para la celda y la hora. La muestra conserva 2.459 filas de 162 fechas y 102 sitios.

## B. Procedencia y test de fuente

| Archivo local | Productor y URL | Descarga | SHA-256 |
|---|---|---|---|
| `data/raw/globe_2024.csv.zip` | NASA Langley/GLOBE, https://zenodo.org/records/18763550/files/2024_GLOBE_AnnualCloudObs_2026-01-05_v3-4.csv.zip?download=1 | 2026-11-05 | `ca88944757b45d1b205c634d8631fdaeb01d54b11acecc88fecccd247ca4adce` |
| `data/raw/power_2024_hourly.json` | NASA POWER, URL de API en README | 2026-11-05 | `9b8b7de561c812e02c1747b98143452390ff62c32ce352bd401c578cbca6857c` |

1. **Descarga trazable.** Las URL primarias están arriba y en el README. `scripts/preparar_datos.py` lee los originales sin depender de Kaggle. `scripts/descargar_fotos.py` obtiene los JPG de `data.globe.gov`.
2. **Búsqueda de espejos.** El 2026-11-05 se buscó `site:kaggle.com/datasets "GLOBE Clouds" "AnnualCloudObs"`; no apareció un archivo equivalente en los resultados. Se usa el fichero del DOI oficial, identificado por SHA-256.
3. **Huella de crudeza.** GLOBE bruto: 180.101 filas; 84.342 con foto arriba y etiqueta en todo el archivo. Recorte unido: 2.459; 839 positivas (34,1 %) y 1.620 negativas (65,9 %); 162 fechas. El filtrado elimina fotos faltantes y categorías ambiguas. `data/processed/verificacion.json` contiene recuentos completos.
4. **Contraste.** No se encontró una réplica exacta; se conserva el nombre y la huella del archivo original para que el docente pueda repetir el contraste.

## C. Checklist de protección de datos

| Comprobación | GLOBE Clouds | NASA POWER |
|---|---|---|
| A. Identificadores personales | En el recorte se mantienen ID de observación y sitio, fecha, ubicación y foto del cielo. Se excluyen nombres, cuentas y columnas ajenas al objetivo. Las fotos descargadas son del cielo; antes de publicar el corpus completo se revisará que no haya personas u otros identificadores. | No contiene registros de personas; solo variables ambientales por celda y hora. |
| B. Datos sensibles | No se usan datos de salud, biométricos ni otros sensibles. | No hay datos sensibles. |
| C. Menores | No se tratan imágenes de personas. | No aplica. |
| D. Base de uso | Datos abiertos de GLOBE; la ficha del DOI declara uso libre en investigación, publicación y aplicaciones con reconocimiento de la fuente. | NASA POWER declara uso sin restricciones y solicita cita. |
| E. Finalidad | Uso académico para entrenar y evaluar una alerta de nubosidad; sin decisiones sobre personas. | Igual. |
| F. Anonimización | La propuesta no publica coordenadas exactas. El CSV local conserva la geolocalización necesaria para reproducir el cruce. No se conservarán metadatos EXIF en copias publicadas. | La celda espacial es ambiental, sin identificación individual. |
| G. Licencia/términos | Condiciones de uso GLOBE/NASA indicadas en la ficha primaria; no se atribuye una licencia CC que la fuente no declara. Atribución obligatoria. | Uso sin restricciones, cita solicitada por NASA POWER. |
| H. Servicios externos | Solo se subirán fotos revisadas, sin personas identificables. No se pegarán datos personales en asistentes de IA. | Datos ambientales aptos para Colab/Drive/GitHub. |
| I. Minimización y conservación | Se conserva el ZIP primario y un CSV recortado; se prevé eliminar los originales al finalizar el curso, salvo obligación de trazabilidad. | Se conserva un año y tres variables horarias; igual criterio de conservación. |
| J. Repositorio | Antes de hacerlo público se revisarán fotos y términos de redistribución. Se puede compartir privado con el docente mientras tanto. | Puede citarse la API y el archivo descargado. |

**Declaración de cada integrante:** Revisé el contenido de este checklist y completaré la revisión de las fotos antes de publicarlas.

| Integrante | Firma (nombre digitado, según indicación del equipo) | Fecha |
|---|---|---|
| David Felipe Tautiva Nieto | David Felipe Tautiva Nieto | 2026-11-05 |
| Isabella Carolina Jimenez | Isabella Carolina Jimenez | 2026-11-05 |
| Juan David Bernal Millot | Juan David Bernal Millot | 2026-11-05 |
