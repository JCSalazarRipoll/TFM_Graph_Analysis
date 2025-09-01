# TFM - Estimación de la Distancia Promedio en Grafos Masivos

Este repositorio contiene el desarrollo del Trabajo de Fin de Máster (TFM) de Juan Camilo Salazar Ripoll, centrado en el estudio de la distancia promedio entre nodos en grafos de distintos tamaños, 
con especial énfasis en grafos masivos como los de Facebook y YouTube.

## Objetivo del proyecto

El objetivo principal es analizar 204 grafos de diferentes tamaños para estudiar cómo se puede calcular o estimar la **distancia promedio entre nodos**. 
Dado que en grafos masivos este valor no se puede calcular directamente por su alto costo computacional, se exploran distintas técnicas de estimación y modelos aproximados para evaluar su precisión y eficiencia.
## Estructura del repositorio

```plaintext
TFM_Graph_Analysis/
│
├── notebooks/          # Notebooks de Google Colab con el desarrollo del análisis
├── src/                # Scripts Python con funciones reutilizables
├── data/               # Conjuntos de datos utilizados (si aplica)
├── docs/               # Documentación adicional e imágenes
│
├── README.md           # Este archivo
├── requirements.txt    # Librerías necesarias para ejecutar el proyecto
└── .gitignore          # Archivos excluidos del repositorio
