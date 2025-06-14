# desarrollo_web_Luciano_Providel
# Tarea 3

## Estructura del Proyecto

```
proyecto/
├── app.py
├── models.py
├── utils.py
├── config.py
├── static/
│   ├── css/
│   │   └── styles.css 
│   ├── js/
│   │   ├── agregar.js 
│   │   ├── listado.js
│   │   └── region_comuna.js 
│   └── images/
│       └── ...
└── templates/  
    ├── base.html
    ├── portada.html
    ├── agregar.html
    ├── listado.html
    └── estadisticas.html
```

### Estadísticas:

La nueva página de estadísticas presenta tres gráficos interactivos generados dinámicamente desde la base de datos:

**Gráfico de Líneas - Actividades por Día:**
* Muestra la cantidad de actividades por cada día
* Eje X: fechas de las actividades
* Eje Y: cantidad de actividades
* Implementado con Chart.js tipo 'line'

**Gráfico de Torta - Actividades por Tipo:**
* Distribución de actividades según su tema
* Cada segmento representa un tipo de actividad (música, deporte, juegos, etc.)
* Colores diferenciados para cada categoría
* Implementado con Chart.js tipo 'pie'

**Gráfico de Barras - Actividades por Mes y Horario:**
* Tres barras por cada mes mostrando distribución horaria
* Mañana: 6:00 - 11:59
* Mediodía: 12:00 - 17:59  
* Tarde: 18:00 - 5:59
* Implementado con Chart.js tipo 'bar'

Los gráficos se generan usando JavaScript con AJAX, obteniendo los datos desde APIs REST del servidor que consultan directamente la base de datos.

### Sistema de Comentarios:

Se implementó un sistema completo para agregar y visualizar comentarios en las actividades:

**Agregar Comentario:**
* Formulario integrado en el detalle de cada actividad
* Campos: nombre (3-80 caracteres) y texto del comentario (mínimo 5 caracteres)
* Validación en cliente (JavaScript) y servidor (Flask)
* Envío asíncrono con fetch() sin recargar la página
* Feedback inmediato de éxito o errores

**Listado de Comentarios:**
* Visualización automática de comentarios asociados a cada actividad
* Ordenados por fecha (más recientes primero)
* Muestra: nombre del comentarista, fecha/hora y texto del comentario
* Carga asíncrona al seleccionar una actividad

## Portada:

Sin cambios respecto a la Tarea 2. La tabla muestra las últimas 5 actividades agregadas a la base de datos con los datos: inicio, término, comuna, sector, tema y foto.

El header se mantiene gestionado a través de la plantilla base (base.html) que se extiende en todas las páginas, ahora incluyendo el enlace a "Estadísticas".

## Agregar actividad:

Sin cambios respecto a la Tarea 2. El formulario mantiene la misma funcionalidad de carga dinámica de regiones/comunas, validaciones y feedback mediante mensajes flash.

## Lista de actividades:

Se mantiene la funcionalidad base de la Tarea 2, pero se agregó el sistema de comentarios integrado. Cada fila sigue siendo clickeable para mostrar el detalle, pero ahora incluye:

* Sección de comentarios con formulario para agregar nuevos
* Lista de comentarios existentes con fecha y autor
* Validaciones cliente-servidor para nuevos comentarios
* Interfaz actualizada dinámicamente con AJAX

## Validaciones:

Se mantienen las validaciones existentes y se agregaron nuevas para comentarios:

1. **Validación en el cliente**: JavaScript valida formularios antes de envío
2. **Validación en el servidor**: Flask valida datos recibidos
3. **Validación en la base de datos**: Restricciones en modelos
4. **Nuevas validaciones para comentarios**:
   - Nombre: obligatorio, 3-80 caracteres
   - Texto: obligatorio, mínimo 5 caracteres
   - Actividad válida: verificación de existencia

## Instalación y Configuración:

Para configurar el proyecto, cree un espacio virtual e instale las librerías que ocupe:

```bash
python -m venv venv

venv\Scripts\activate
   
pip install flask flask-sqlalchemy mysqlclient Werkzeug
```

La configuración de base de datos la hice desde MySQL Workbench, donde agregue `tabla-comentario.sql`.

Finalmente la aplicación corre con el comando:

```bash
python app.py
```
