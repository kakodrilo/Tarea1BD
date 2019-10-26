----------------------------------
=====> SANSTORE v1.1.0 <=====    
----------------------------------
23/07/2019
----------------------------------

Joaquín Castillo Tapia       201773520-1
Luis Elicer Krause           201773513-9
María Paz Morales Llopis     201773505-8

----------------------------------

REQUISITOS:
==================================================

- Windows 10 o superior (64-bits)
- Oracle Database 18c (64-bits)
- Python 3.6.8 (64-bits)
  -> Librerías:
     - pyodbc
     - csv
     - random
     - subprocess

==================================================

INSTALACIÓN:
==================================================

- Crear una Base da Datos en Oracle Database 18c con nombre "T1BD" y contraseña "Equipo32019"
- Agregar la base de datos creada como nuevo origen de datos en el Administrador de origen de datos ODBC (64-bits) del sistema.
  * el nombre debe ser "T1BD" y el USER ID "system"
- Ejecutar el archivo "LOAD_DB.py" que carga las tablas de datos
  * Los archivos csv "Sansanoplay.csv" y "Nintendo.csv" deben estar en el mismo directorio
- Ejecutar "SANSANOPLAY-NINTENDO.py" que es la aplicación de usuario.

==================================================

INSTRUCCIONES DE USO:
==================================================

Esta aplicación tiene por objetivo un mejor manejo de datos de la tienda Sansanoplay, 
trabajando con la base de datos de videojuegos de Nintendo y realizando distintas operaciones 
que modifican dicha base de datos como acomode al usuario.

La aplicación soporta las siguientes funciones:
- Agregar un videojuego a la base de datos.
- Buscar y leer los datos de un juego.
- Actualizar (1 o más) datos de un videojuego en particular.
- Borrar los datos de un juego.
- Realizar venta de un juego.
- Realizar una devolución de un juego.
- Borrar la base de datos.

Además, la aplicación permite realizar las siguientes consultas:
- 5 juegos exclusivos más caros.
- 3 géneros más vendidos localmente.
- 3 géneros más vendidos globalmente.
- 3 desarrolladoras con más ventas.
- Juegos con mejor rating.

Al iniciar la aplicación se desplegará un menú con las opciones soportadas por esta. 

Para realizar la operación deseada se debe ingresar el número que aparece a la izquierda de la operación. 

Al seleccionar la operación deseada se detallarán instrucciones en pantalla de cómo se debe operar.

Una vez seleccionada la función no se puede volver al menú principal hasta que se realice dicha operación.

Cuando termine de realizar todas las operaciones deseadas, presione 13 para cerrar la aplicación.

IMPORTANTE: Borrar la base de datos es una operación irreversible, no lo haga a menos que esté seguro.



CONSIDERACIONES:
==================================================

- Se ignoran las fechas no definidas, es decir, el atributo queda como null
- La única forma de modificar las ventas de un juego es a través de una venta o devolución
- El stock se actualiza automáticamente cuando baja de 10
