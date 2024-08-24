# Proyecto de Predicción de Pasajeros

Este proyecto implementa un modelo de machine learning para la predicción de características de pasajeros, encapsulado en una API desarrollada con FastAPI. El proyecto está estructurado para soportar tanto el desarrollo interactivo como la producción, utilizando ambientes Python diferenciados para cada propósito.

## Autores

Este proyecto fue desarrollado por:

- Luis Pedro Gonzalez
- Juan Angel Carrera
- Mariano Reyes
- Esteban Aldana
- Juan Carlos Bajan


## Estructura del Proyecto

El proyecto está organizado en los siguientes directorios:

- **scripts**: Contiene los Jupyter notebooks utilizados para la creación interactiva del modelo de machine learning. Además, incluye scripts de Python que definen las clases y funciones necesarias para la construcción, entrenamiento y evaluación del modelo. Este directorio es clave durante la fase de desarrollo del modelo, donde se iteran distintas versiones y se ajustan los parámetros para optimizar su rendimiento.

- **app**: Este directorio contiene la lógica para cargar el modelo entrenado y las configuraciones necesarias para desplegar la API utilizando FastAPI. El servidor de la API se levanta utilizando `uvicorn`. 
- **tests**: Contiene los tests de la API escritos utilizando `pytest`.
## Python Environments

El proyecto utiliza entornos Python para diferenciar entre producción y desarrollo:

- **penv**: Este entorno está configurado para ser utilizado en producción. Incluye solo las dependencias necesarias para ejecutar la API y el modelo, asegurando un ambiente limpio y eficiente para el despliegue.

- **devenv**: Este entorno está diseñado para el desarrollo, especialmente para aquellos que trabajan en notebooks y ejecutan tests. Incluye herramientas adicionales para la depuración, análisis y pruebas, facilitando el trabajo durante la fase de desarrollo.


## Uso del Proyecto

### 1. Configuración de los Entornos

Asegúrate de activar el entorno Python adecuado para tu caso de uso:

- Para producción: 
 ```bash
  source penv/Scripts/activate
 ```
- Para desarrollo: 
 ```bash
 source devenv/Scripts/activate
 ```


### 2. Ejecución de la API
Para levantar la API, asegúrate de estar en el entorno de producción (o desarrollo si estás en fase de testeo), y ejecuta:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```


### 3. Ejecución de los Tests

```bash
cd /tests
```

```bash
pytest test.py --junitxml=report.xmlte
```

### 4. Creación y Entrenamiento del Modelo
Para la fase de desarrollo del modelo, se utilizaron los notebooks y scripts disponibles en el directorio scripts para iterar sobre distintas versiones del modelo, ajustar parámetros, y realizar pruebas. 