# desarrollo_web_Luciano_Providel
# Tarea 1

## Portada:

Para la portada decidí hacer una tabla simple que contuviera los datos de las actividades según el enunciado:
* Término
* Comuna
* Sector
* Tema
* Foto
  
Estos datos los rellene con eventos a los cuales asisto normalmente (principalmente torneos de TCG).
También utilice un header que lleva a las distintas páginas de la aplicación. Este header se replica en todas las páginas, reemplazando la sección actual por un botón que devuelve al inicio.

## Agregar actividad:

Para agregar la actividad realice un formulario dividido por las secciones que aparecen en el enunciado. Para llenar la información de regiones y comunas utilice el archivo region_comuna.js que se encuentra en el material docente. El llenado de esta lista lo hice mediante una función en javascript que rescata el nombre de la región y las comunas que se encuentran en ella. 

Para validar la información utilice validadores en javascript que verificaban que los campos obligatorios no estuvieran vacíos y además que el formato coincidiera con lo solicitado. Además decidí que para los casos donde es necesario agregar texto como en las redes sociales o cuando se selecciona otro tema para el evento, se dejara un div vacío, que al momento de ser cambiado, llene el div, haciendo que aparezca un recuadro de texto el cual el usuario debe llenar. Otra funcion es la de agregar fotos que se añade un boton mientras no se alcance el maximo.

Finalmente al enviar el formulario, se chequea que todo esta bien, y si lo esta se oculta el form para mostrar el mensaje de confirmación, el cual tambien inicialmente esta vacío, pero se llena al momento de su uso.
Si no, se indica que el formulario esta malo.

## Lista de actividades:

Para esta sección se creo una tabla vacía con los campos, que luego se rellenan con los datos dentro del javascript y se le añade a cada uno un listener que se activa en click. Al hacer click en la actividad, se oculta el listado de actividades y se rellena con la información asociada a la actividad, mostrando los datos del enunciado y las fotos asociadas, y al hacer click se abre un modal con la imagen en un tamaño mayor, con un boton para volver atrás. Además, aparece un botón para volver al listado, que funciona ocultando los detalles y volviendo a mostrar el listado inicial.

## Estadisticas:

Aqui solo fue crear una pagina con secciones que indican el titulo seguido con una imagen con el gráfico.

## CSS:

No quise gastar mucho tiempo en el diseño por lo que cambie un par de colores para el header y ajuste los tamaños de las tablas.
