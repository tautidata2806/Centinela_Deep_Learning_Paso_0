# Bitácora de IA y decisiones

**Fecha:** 2026-11-05. **Herramienta:** Codex. **Equipo:** David Felipe Tautiva Nieto, Isabella Carolina Jimenez y Juan David Bernal Millot. **Autoría:** cada integrante debe revisar, corregir y firmar su parte de lo que entregue.

| Consulta o ayuda | Resultado de la IA | Decisión y verificación |
|---|---|---|
| Elegir tema fácil y viable | Primero sugirió mosquitos e incendios. | **Rechazados**: el primero ya existía. En incendios, el docente señaló la resolución agregada de POWER, el balance real y filtro VIIRS pendientes, las licencias por precisar y scripts ausentes. La nueva propuesta v2 cambia de problema y muestra acoplamiento reproducible. |
| Evaluar nubosidad | Sugirió GLOBE Clouds + NASA POWER. | **Aceptado tras verificar** descarga real, columnas, 2.459 cruces y diez fotos accesibles. |
| Definir etiqueta | Propuso nube alta sí/no. | **Ajustado** a categorías originales `broken`/`overcast` frente a cuatro categorías de menor cobertura; se excluyó `obscured`. |
| Conectar fuentes | Propuso foto de GLOBE más serie horaria POWER. | **Verificado** con `scripts/preparar_datos.py`; la serie usada termina una hora antes de la foto. Se declaró que la unión es espacial agregada. |
| Unidades de irradiancia | Una primera versión nombró la unidad como kWh/m². | **Corregido** a Wh/m² tras revisar `parameters.ALLSKY_SFC_SW_DWN.units` en el JSON oficial. El CSV final usa `power_irradiance_prior_wh_m2`. Este es un error real detectado en la ayuda de IA. |
| Redacción de propuesta y anexos | La IA preparó borradores. | Se incorporaron los tres nombres dados por el equipo. **Pendiente de revisión personal**: sentido del cliente, términos de entrega del campus y conformidad con los nombres digitados en la firma. No se presenta como trabajo sin asistencia de IA. |
| Preparar corpus visual | Se propuso descargar solo diez fotos para el Paso 0 y dejar un script para el resto. | **Ampliado por instrucción del equipo**: se descargaron las 2.459 fotos del recorte desde GLOBE y se validaron. El equipo decidió incluir datos y fotos al copiar el proyecto a su propio repositorio; la guía de sustentación queda excluida. |

**Datos compartidos con la IA:** esquema, conteos y diez filas de datos ambientales públicos de la muestra; no se compartieron datos personales.
