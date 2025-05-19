# desarrollo_web_Luciano_Providel
# Tarea 2

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
```

## Portada:

Para la portada, la tabla muestra las últimas 5 actividades agregadas a la base de datos. Los datos que se muestran son:
* Inicio
* Término
* Comuna
* Sector
* Tema
* Foto (primera foto de cada actividad)

El header ahora se maneja a través de una plantilla base (base.html) que se extiende en todas las páginas en vez de ir escribiendo el codigo en cada página.

## Agregar actividad:

El formulario para agregar actividades ahora está conectado a la base de datos mediante Flask. Las principales características incluyen:

- Carga dinámica de regiones y comunas desde la base de datos
- Validación de formularios tanto en el cliente (JavaScript) como en el servidor (Flask)
- Feedback de éxito o error mediante mensajes flash

Las validaciones siguen siendo como los de la primera tarea.

## Lista de actividades:

La lista de actividades ahora se genera dinámicamente desde la base de datos, y como la T1, cada fila de la tabla es clickeable y muestra el detalle completo de la actividad correspondiente, ocultando la tabla y mostrando un div con toda la información.

## Validaciones:

Se implementaron validaciones en varios niveles:

1. **Validación en el cliente**: JavaScript valida los formularios antes de enviarlos
2. **Validación en el servidor**: Flask valida nuevamente los datos recibidos
3. **Validación en la base de datos**: Restricciones en el modelo de datos

## API REST:

La aplicación proporciona endpoints API para:

- Obtener todas las regiones (`/api/regiones`)
- Obtener comunas por región (`/api/comunas/<region_id>`)
- Obtener detalles de una actividad (`/actividad/<id>`)

## Instalación y Configuración:

Para configurar el proyecto tuve que crear un entorno virtual e instalar las librerias que ocuparia para la tarea:

```bash
python -m venv venv

venv\Scripts\activate
   
pip install flask flask-sqlalchemy mysqlclient Werkzeug

```

Luego tuve que configurar la base de datos para que esta cargara los datos de los sql del enunciado. Para esto tuve que descargar MySQL y MySQL Workbench.

```bash
mysql -u root -p
CREATE DATABASE tarea2;
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Y finalmente ejecuto la aplicación con el comando:

```bash
python app.py
```
