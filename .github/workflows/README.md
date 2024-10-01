# Descripción del Workflow de CI/CD
Este documento proporciona una explicación detallada del workflow de CI/CD definido en `ci-cd-app.yml`. Este workflow está diseñado para automatizar el proceso de construcción, etiquetado y despliegue de una imagen Docker en Amazon Elastic Container Registry (ECR), así como para actualizar instancias en AWS mediante AWS Systems Manager (SSM).

## Desencadenadores del Workflow
El workflow se ejecuta automáticamente cuando se realiza un push en la rama `main` del repositorio:

```yaml
on:
  push:
    branches:
      - main
```

## Estrategia de Construcción
El job `build` utiliza una matriz de estrategias para ejecutar el workflow en múltiples regiones de AWS:
```yaml
strategy:
  matrix:
    region: [us-east-1, us-east-2]
```

Esto significa que el workflow se ejecutará dos veces, una para cada región especificada en la matriz (`us-east-1` y `us-east-2`).

## Pasos del Job `build`
El job `build` se ejecuta en un runner de `ubuntu-latest` y sigue los siguientes pasos:

### 1. Checkout del Repositorio
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```
Este paso clona el repositorio en el runner para acceder al código fuente necesario para construir la imagen Docker.



### 2. Configurar Credenciales de AWS
```yaml
- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ${{ matrix.region }}
```
Configura las credenciales de AWS necesarias para interactuar con los servicios de AWS. Utiliza las credenciales almacenadas en los secretos del repositorio y establece la región de AWS según la matriz.

### 3. Iniciar Sesión en Amazon ECR
```yaml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v2
```
Este paso autentica el runner con Amazon ECR, permitiendo que se puedan empujar imágenes Docker al repositorio ECR.


### 4. Construir, Etiquetar y Empujar la Imagen a Amazon ECR
```yaml
- name: Build, tag, and push image to Amazon ECR
  env:
    ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
    ECR_REPOSITORY: sento-${{ matrix.region }}-processor-ecr
    IMAGE_TAG: latest
    IMAGE_SHA: ${{ github.sha }}
  run: |
    docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
    docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
    docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_SHA
    docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_SHA
```
Este paso realiza las siguientes acciones:

* **Construcción de la imagen Docker:** Utiliza el Dockerfile en el directorio actual para construir la imagen.
* **Etiquetado de la imagen:** La imagen se etiqueta con `latest` y con el SHA del commit actual (`IMAGE_SHA`).
* **Empuje de la imagen a ECR:** La imagen etiquetada se empuja al repositorio ECR correspondiente en la región especificada.


### 5. Actualizar las Instancias
```yaml
- name: Updating instance statics
  run: |
    aws ssm send-command --document-name "${{ matrix.region }}-pull-image-document" --document-version "\$LATEST" --targets '[{"Key":"tag:Environment","Values":["QA"]},{"Key":"tag:OS","Values":["Ubuntu"]}]' --parameters '{"image":["AI"],"region":["${{ matrix.region }}"]}' --timeout-seconds 600 --max-concurrency "50" --max-errors "0"  --region ${{ matrix.region }}
    aws ssm send-command --document-name "${{ matrix.region }}-pull-image-document" --document-version "\$LATEST" --targets '[{"Key":"tag:Environment","Values":["QA"]},{"Key":"tag:OS","Values":["Linux"]}]' --parameters '{"image":["AI"],"region":["${{ matrix.region }}"],"os":["Linux"]}' --timeout-seconds 600 --max-concurrency "50" --max-errors "0"  --region ${{ matrix.region }}
```
Este paso envía comandos a las instancias de AWS EC2 utilizando AWS Systems Manager (SSM):

* **Primer Comando:** Actualiza las instancias con las etiquetas `Environment=QA` y `OS=Ubuntu`.
* **Segundo Comando:** Actualiza las instancias con las etiquetas `Environment=QA` y `OS=Linux`.
Ambos comandos utilizan un documento SSM llamado `${{ matrix.region }}-pull-image-document` para ejecutar acciones en las instancias, como actualizar la imagen Docker.

# Reflexión sobre la Integración de Herramientas CI/CD en Proyectos de Machine Learning
La integración de herramientas de CI/CD en proyectos de Machine Learning es esencial para garantizar la reproducibilidad, escalabilidad y eficiencia en el ciclo de vida del desarrollo de modelos. Al automatizar procesos como el entrenamiento, validación y despliegue de modelos, se logra:
  
* **Consistencia:** Los modelos se entrenan y despliegan bajo entornos controlados, reduciendo la posibilidad de errores humanos.
* **Escalabilidad:** Facilita el manejo de grandes volúmenes de datos y modelos complejos al automatizar tareas repetitivas.
* **Colaboración:** Mejora la colaboración entre equipos multidisciplinarios al proporcionar un pipeline unificado.
* **Feedback Rápido:** Permite identificar y corregir problemas rápidamente mediante pruebas automatizadas y despliegues continuos.

En resumen, la integración de CI/CD en proyectos de Machine Learning no solo optimiza el flujo de trabajo sino que también potencia la entrega de soluciones más robustas y eficientes.