# Tablero Power BI: copia local posterior a la entrega

**Archivo de trabajo:** `outputs/TransMilenio_postentrega_2026-11-25_filtros.pbix`. Es una copia **local** de nueve páginas, distinta del PBIX de ocho páginas descrito en [la documentación del 24/11](tablero_powerbi_2026-11-24.md). Esta nota no indica que la copia nueva se haya compartido ni entregado. `outputs/` está excluido de Git.

## Páginas y navegación

1. **Entradas y oferta**: portada con las curvas de entradas registradas y pasos programados. Tiene filtros interactivos de **fecha** y **tipo de día**.
2. **Mapa de entradas**: mapa Azure actualizado con la distribución espacial de validaciones que tienen coordenadas.
3. **Mapa social**: mapa Azure actualizado con indicadores de contexto por localidad, no atributos individuales de pasajeros.
4. **Pico y valle**: comparación de las franjas propuestas entre días hábiles y fines de semana.
5. **Entradas por paso**: relación entre entradas y pasos programados para filas comparables.
6. **Contexto territorial**: indicadores de localidades y su relación descriptiva con las estaciones ubicadas allí.
7. **Estaciones**: comparación y consulta por estación.
8. **Método y límites**: fuentes, definición del indicador, cobertura y cautelas.
9. **Indicadores**: tarjetas KPI con filtros interactivos de **fecha** y **tipo de día**.

Los filtros de portada e Indicadores se comprobaron en esas páginas; no se afirma que estén sincronizados con todas las demás. Las franjas usadas son pico **06:00–08:59 y 16:00–18:59** y valle **09:00–15:59**; son rangos de análisis provisionales, no una definición oficial del sistema.

## Indicadores auditados para la vista completa

| Tarjeta | Valor | Lectura correcta |
| --- | ---: | --- |
| Entradas registradas | 9.205.097 | Validaciones, no pasajeros únicos. |
| Entradas comparables | 8.065.892 | Entradas con al menos un paso programado emparejado por fecha, hora y estación. |
| Pasos programados comparables | 1.312.035 | Pasos de esas filas comparables, no toda la oferta de la red. |
| Entradas por paso comparable | 6,15 | 8.065.892 ÷ 1.312.035, redondeado. |
| Cobertura de entradas | 87,62 % | 8.065.892 ÷ 9.205.097; el resto no se interpreta como cero buses. |

Las cifras corresponden **solo al 18–23/11/2026**. La [auditoría de los CSV del tablero](auditoria_datos_tablero_2026-11-25.md) validó 17.503 claves únicas de fecha–hora–estación y la coherencia de las tablas derivadas. El 18 utiliza el CSV corregido de Alejandro: su denominador todavía no es plenamente reproducible desde el GTFS local y la regla documentada. Los mapas tienen cobertura parcial: 8.160.699 de 9.205.097 entradas tienen coordenadas; 133 de 151 estaciones tienen localidad y la comparación territorial muestra 18 localidades. Ausencia de un punto en el mapa no significa demanda cero. La encuesta es de 2021 y describe residentes de la localidad, no a los usuarios que validaron en 2026. Ni la razón ni los mapas miden puntualidad, ocupación o causalidad.
