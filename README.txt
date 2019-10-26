----------------------------------
=====> SANSTORE v1.1.0 <=====    
----------------------------------
23/07/2019
----------------------------------

Joaqu�n Castillo Tapia       201773520-1
Luis Elicer Krause           201773513-9
Mar�a Paz Morales Llopis     201773505-8

----------------------------------

REQUISITOS:
==================================================

- Windows 10 o superior (64-bits)
- Oracle Database 18c (64-bits)
- Python 3.6.8 (64-bits)
  -> Librer�as:
     - pyodbc
     - csv
     - random
     - subprocess

==================================================

INSTALACI�N:
==================================================

- Crear una Base da Datos en Oracle Database 18c con nombre "T1BD" y contrase�a "Equipo32019"
- Agregar la base de datos creada como nuevo origen de datos en el Administrador de origen de datos ODBC (64-bits) del sistema.
  * el nombre debe ser "T1BD" y el USER ID "system"
- Ejecutar el archivo "LOAD_DB.py" que carga las tablas de datos
  * Los archivos csv "Sansanoplay.csv" y "Nintendo.csv" deben estar en el mismo directorio
- Ejecutar "SANSANOPLAY-NINTENDO.py" que es la aplicaci�n de usuario.

==================================================

INSTRUCCIONES DE USO:
==================================================

Esta aplicaci�n tiene por objetivo un mejor manejo de datos de la tienda Sansanoplay, 
trabajando con la base de datos de videojuegos de Nintendo y realizando distintas operaciones 
que modifican dicha base de datos como acomode al usuario.

La aplicaci�n soporta las siguientes funciones:
- Agregar un videojuego a la base de datos.
- Buscar y leer los datos de un juego.
- Actualizar (1 o m�s) datos de un videojuego en particular.
- Borrar los datos de un juego.
- Realizar venta de un juego.
- Realizar una devoluci�n de un juego.
- Borrar la base de datos.

Adem�s, la aplicaci�n permite realizar las siguientes consultas:
- 5 juegos exclusivos m�s caros.
- 3 g�neros m�s vendidos localmente.
- 3 g�neros m�s vendidos globalmente.
- 3 desarrolladoras con m�s ventas.
- Juegos con mejor rating.

Al iniciar la aplicaci�n se desplegar� un men� con las opciones soportadas por esta. 

Para realizar la operaci�n deseada se debe ingresar el n�mero que aparece a la izquierda de la operaci�n. 

Al seleccionar la operaci�n deseada se detallar�n instrucciones en pantalla de c�mo se debe operar.

Una vez seleccionada la funci�n no se puede volver al men� principal hasta que se realice dicha operaci�n.

Cuando termine de realizar todas las operaciones deseadas, presione 13 para cerrar la aplicaci�n.

IMPORTANTE: Borrar la base de datos es una operaci�n irreversible, no lo haga a menos que est� seguro.



CONSIDERACIONES:
==================================================

- Se ignoran las fechas no definidas, es decir, el atributo queda como null
- La �nica forma de modificar las ventas de un juego es a trav�s de una venta o devoluci�n
- El stock se actualiza autom�ticamente cuando baja de 10
