# Proyecto Centinela: nubosidad alta para operación solar

**Curso:** Redes Neuronales – Deep Learning · Universidad Santo Tomás  
**Entrega actual:** Propuesta de Datos, Paso 0, versión **v2**  
**Equipo:** David Felipe Tautiva Nieto, Isabella Carolina Jimenez y Juan David Bernal Millot  
**Estado:** propuesta preparada para aprobación del docente. Todavía no se ha entrenado un modelo.

## 1. Idea del proyecto

Queremos identificar, a partir de una fotografía del cielo, si la nubosidad observada es alta. El resultado sería una alerta para que el operador de una instalación solar pequeña revise su expectativa inmediata de generación. **No estamos prediciendo la producción eléctrica ni el tiempo de mañana.**

La etiqueta es binaria y procede de las categorías originales de GLOBE:

| Resultado | Categorías GLOBE | Registros del recorte |
|---|---|---:|
| Nubosidad alta: sí | `broken`, `overcast` | 839 |
| Nubosidad alta: no | `none`, `few`, `isolated`, `scattered` | 1.620 |

Se excluye `obscured` porque una vista obstruida no demuestra que el cielo esté cubierto por nubes. El recorte final contiene **2.459 observaciones de 2024**, distribuidas en **162 fechas y 102 sitios**.

## 2. Fuentes y comprobaciones realizadas

**Fotografías y etiqueta:** [GLOBE Clouds, NASA Langley, archivo anual 2024 v3.4](https://doi.org/10.5281/zenodo.18763550). Descargamos el archivo original, que contiene **180.101 observaciones**, y seleccionamos las que tienen foto hacia arriba, categoría utilizable, ubicación dentro del área elegida y hora válida. Descargamos las **2.459 fotografías** del recorte desde sus URL originales de GLOBE. El script de verificación confirmó que están presentes y tienen estructura JPG válida; el manifiesto conserva URL, tamaño y SHA-256 de cada una.

**Serie temporal:** [NASA POWER, API horaria](https://power.larc.nasa.gov/docs/services/api/temporal/hourly/). Descargamos **8.784 horas de 2024** de temperatura (`T2M`), humedad relativa (`RH2M`) e irradiancia solar (`ALLSKY_SFC_SW_DWN`) para el punto 28,625° N, 81,625° O. La irradiancia horaria está expresada en **Wh/m²**, como indica la respuesta de la API.

**Acoplamiento comprobado:** Cada fotografía del área 28,5–28,75° N y 81,75–81,5° O se une con la hora de POWER inmediatamente anterior. `data/processed/anexo_a_10_uniones.csv` muestra diez casos de **fechas distintas** con foto, etiqueta y variables de la serie. La unión es espacialmente agregada: POWER representa una celda, no el punto exacto de cada cámara.

## 3. Estructura de la carpeta

```text
proyecto_centinela/
├── README.md                         Descripción, fuentes y reproducción
├── propuesta.md                      Texto editable de la propuesta v2
├── propuesta_para_entregar.html      Versión imprimible de una página
├── anexos.md                         Prueba de unión, procedencia y datos personales
├── bitacora_ia.md                    Ayuda recibida, correcciones y decisiones
├── Entrega_Paso0_Centinela_Nubosidad.zip
│                                     Paquete pequeño para el Paso 0
├── data/
│   ├── raw/
│   │   ├── globe_2024.csv.zip        Archivo original de GLOBE
│   │   ├── power_2024_hourly.json    Respuesta original de NASA POWER
│   │   └── photos/                   Las 2.459 fotografías descargadas
│   └── processed/
│       ├── observaciones_unidas.csv  Recorte y unión de las dos fuentes
│       ├── anexo_a_10_uniones.csv    Diez filas de evidencia
│       ├── manifiesto_fotos.csv      URL, tamaño y huella de cada fotografía
│       ├── verificacion.json        Conteos y huellas de fuentes originales
│       └── verificacion_fotos.json  Resultado de la revisión de JPG
├── scripts/
│   ├── descargar_fuentes.py          Obtiene GLOBE y POWER de sus fuentes
│   ├── preparar_datos.py            Aplica filtros, etiqueta y unión horaria
│   ├── descargar_fotos.py           Obtiene las fotografías de GLOBE
│   └── verificar_fotos.py           Revisa archivos y genera el manifiesto
├── output/pdf/
│   └── Propuesta_Datos_Centinela_Nubosidad.pdf
│                                     Propuesta v2 de una página
├── entrega_paso0/                   Copia de los documentos del ZIP
└── references/                      Plantilla original y metadatos del DOI
```

El **ZIP del Paso 0 no es una copia de todo el proyecto**. Incluye el PDF de una página, los anexos, la bitácora, el CSV de diez uniones y diez fotos de muestra. El repositorio completo muestra además las fuentes, las 2.459 fotos y los scripts.

## 4. Cómo reproducir los datos

Los scripts usan Python 3.10 o posterior y solo la biblioteca estándar. Desde la raíz del proyecto:

```powershell
python scripts/descargar_fuentes.py
python scripts/preparar_datos.py
python scripts/descargar_fotos.py --all
python scripts/verificar_fotos.py
```

`descargar_fuentes.py` no sobrescribe archivos ya presentes. `preparar_datos.py` vuelve a generar el CSV unido, el anexo de diez filas y los conteos. `descargar_fotos.py` omite fotos ya descargadas. `verificar_fotos.py` comprueba los JPG y genera el manifiesto de huellas. Las URL originales se encuentran en los scripts y en los archivos de evidencia.

## 5. Alcance de cada fase y límites

En la **Fase 1**, la fotografía se resumirá en varios números de color y brillo para entrenar un MLP, después de obtener la aprobación de esta propuesta. En la **Fase 2**, la rama visual podrá usar las imágenes completas y la rama temporal las horas anteriores de POWER. Las seis categorías originales ofrecen más de tres grupos para el trabajo visual posterior.

La categoría de nubosidad la informa una persona y puede variar entre observadores. Algunas fechas y sitios aportan muchas fotos; una partición aleatoria por imagen podría inflar el resultado. Por eso, al modelar se separarán fechas entre entrenamiento, validación y prueba y se revisará el desempeño por sitio. La serie POWER es agregada y puede asignar el mismo valor a varias fotografías. La propuesta no afirma un pronóstico futuro ni una medición de energía producida.

## 6. Procedencia y uso responsable

Los datos provienen de GLOBE/NASA y NASA POWER, no de Kaggle. Las fuentes, fechas de descarga y huellas SHA-256 figuran en `anexos.md` y `data/processed/verificacion.json`. La ficha de GLOBE declara uso libre para investigación y aplicaciones con reconocimiento de la fuente, sin una licencia CC numerada explícita; POWER permite uso y solicita cita. Esta diferencia se declara tal como aparece en las fuentes y podrá ser objeto de ajuste por el docente.

Las fotografías son del cielo; se verificó su formato, pero una comprobación de formato **no reemplaza** la revisión visual de privacidad antes de difundir imágenes. El checklist de protección de datos está en `anexos.md`. La bitácora registra la asistencia de IA y una corrección de unidades detectada durante la preparación.
