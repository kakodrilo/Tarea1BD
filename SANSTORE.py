import pyodbc
import random
import subprocess
subprocess.call('', shell=True)

'''---------- Colores ----------'''

n = '\033[0;39m'
negro = '\033[0;30m'
rojo = '\033[0;31m'
v = '\033[0;32m'
amarillo = '\033[0;33m'
azul = '\033[0;34m'
morado = '\033[0;35m'
cyan = '\033[0;36m'

'''-------------------------------'''


conn = pyodbc.connect('DSN=T1BD;UID=system;PWD=Equipo32019;CHARSET=UTF8')
cur = conn.cursor()

'''----------- VISTAS ---------------'''

'''----> Top Rating max <----'''

cur.execute('''
CREATE OR REPLACE VIEW top_rait AS
SELECT nombre,fecha_estreno, rating, id FROM nintendo 
WHERE rating = (SELECT MAX(rating) FROM nintendo)
ORDER BY fecha_estreno ASC;
''')

def top_rait():
    print()
    print(amarillo + "\n  -> TOP JUEGOS CON MEJOR RAITING ORDENADOS POR FECHA <-"+n)
    print()
    tabla = cyan+" {0}"+n+" | "+v+"{1}"+n+" | {2}"+n+" | "+amarillo+"{3}"
    cur.execute('SELECT * FROM top_rait')
    print(tabla.format('ID','Nombre','Fecha Lanzamiento','Rating'))
    for i in cur:
        print(tabla.format(i[3],i[0],str(i[1]).split()[0],i[2]))
    input(morado+"\n [Enter para continuar]"+n)
    

'''----> Top 5 Exclusivos Mas Caros <----'''

cur.execute('''
CREATE OR REPLACE VIEW top_5_ex AS 
SELECT * FROM (SELECT nintendo.nombre, sansanoplay.precio, nintendo.id
FROM nintendo INNER JOIN sansanoplay ON nintendo.id = sansanoplay.id
WHERE nintendo.exclusividad = 'Si'
ORDER BY sansanoplay.precio DESC)
WHERE ROWNUM <= 5;
''')

def top_5_ex():
    print()
    print(amarillo + "\n  -> TOP 5 JUEGOS EXCLUSIVOS MAS CAROS <-"+n)
    print()
    tabla = cyan+" {0}"+n+" |"+v+" {1}"+n+" | {2} "
    cur.execute('SELECT * FROM top_5_ex')
    print(tabla.format('ID','Nombre','Precio'))
    for i in cur:
        print(tabla.format(i[2],i[0],i[1]))
    input(morado+"\n [Enter para continuar]"+n)
    

'''----> Top 3 Generos Ventas Locales <----'''

cur.execute('''
CREATE OR REPLACE VIEW top_3_genloc AS
SELECT * FROM (SELECT n.genero, SUM(s.vendidos)
FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id
GROUP BY n.genero
ORDER BY SUM(s.vendidos) DESC)
WHERE ROWNUM <= 3;
''')

def top_3_genloc():
    print()
    print(amarillo + "\n  -> TOP 3 GENEROS CON MAS VENTAS LOCALES <-"+n)
    print()
    tabla = amarillo+" {0}"+n+" | {1} "
    cur.execute('SELECT * FROM top_3_genloc')
    print(tabla.format('Genero','Ventas Locales'))
    for i in cur:
        print(tabla.format(i[0],str(int(i[1]))))
    input(morado+"\n [Enter para continuar]"+n)


'''----> Top 3 Generos Ventas Globales <----'''

cur.execute('''
CREATE OR REPLACE VIEW top_3_genglob AS
SELECT * FROM (SELECT genero, SUM(ventas_globales)
FROM nintendo n
GROUP BY genero
ORDER BY SUM(ventas_globales) DESC)
WHERE ROWNUM <= 3;
''')

def top_3_genglob():
    print()
    print(amarillo + "\n  -> TOP 3 GENEROS CON MAS VENTAS GLOBALES <-"+n)
    print()
    tabla = amarillo+" {0}"+n+" | {1} "
    cur.execute('SELECT * FROM top_3_genglob')
    print(tabla.format('Genero','Ventas Globales'))
    for i in cur:
        print(tabla.format(i[0],str(int(i[1]))))
    input(morado+"\n  [Enter para continuar]"+n)


'''----> Top 3 Desarrolladores Ventas Locales <----'''

cur.execute('''
CREATE OR REPLACE VIEW top_3_desloc AS
SELECT * FROM (SELECT n.desarrollador, SUM(s.vendidos)
FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id
GROUP BY n.desarrollador
ORDER BY SUM(s.vendidos) DESC)
WHERE ROWNUM <= 3;
''')

def top_3_desloc():
    print()
    print(amarillo + "\n  -> TOP 3 DESARROLLADORES CON MAS VENTAS LOCALES <-"+n)
    print()
    tabla = amarillo+" {0}"+n+" | {1} "
    cur.execute('SELECT * FROM top_3_desloc')
    print(tabla.format('Desarrollador','Ventas Locales'))
    for i in cur:
        print(tabla.format(i[0],str(int(i[1]))))
    input(morado+"\n [Enter para continuar]"+n)

'''-----------------------------------------------------------'''

def es_un_int(i):
    try:
        ii = int(i)
        return(1)
    except (SyntaxError, ValueError):
        return(0)

def corregir(s):
    if ("'" in s):
        s = s.replace("'", "''")
    if ("#" in s):
        s = s.replace("#","'||'#'||'")
    return "'"+s+"'"
    

'''----------------------- CRUD ------------------------------'''

def insert_new():
    print()
    i = 1
    print(amarillo+'          -> Agregar Nuevo Juego <-\n'+n)
    print(cyan+' ->'+n+' Ingrese los parametros solicitados.')
    print(cyan+' ->'+n+' Los parametros con'+rojo+' * '+n+'son obligatorios.')
    print(cyan+' ->'+n+' Para los parametros'+cyan+' NO obligatorios'+n+', presione'+morado+' [ENTER]'+n+' si desea omitirlos.\n'+n)
    input(morado+'\n  [Enter para continuar]\n')
 
    atributos = 'id,nombre,genero,desarrollador,publicador'
    valores = '0'
    nombre = ","+corregir(str(input(v+' Nombre'+rojo+'*'+n+': ')))
    while nombre == ",''" or len(nombre)>102:
        print(rojo+" ERROR: Nombre invalido")
        nombre = ","+corregir(str(input(v+' Nombre'+rojo+'*'+n+': ')))
    genero = ","+corregir(str(input(v+' Genero'+rojo+'*'+n+': ')))
    while genero == ",''" or len(genero)>52:
        print(rojo+" ERROR: Genero invalido")
        genero = ","+corregir(str(input(v+' Genero'+rojo+'*'+n+': ')))
    des = ","+corregir(str(input(v+' Desarrollador'+rojo+'*'+n+': ')))
    while des == ",''" or len(des)>52:
        print(rojo+" ERROR: Desarrollador invalido")
        des = ","+corregir(str(input(v+' Desarrollador'+rojo+'*'+n+': ')))
    pbl = ","+corregir(str(input(v+' Publicador'+rojo+'*'+n+': ')))
    while pbl == ",''" or len(pbl)>52:
        print(rojo+" ERROR: Publicador invalido")
        pbl = ","+corregir(str(input(v+' Publicador'+rojo+'*'+n+': ')))
    valores = valores + nombre+genero+des+pbl
    fe = str(input(v+' Fecha de estreno (DD-MM-YYYY)'+n+': '))
    fe = ",TO_DATE('"+fe+"','DD-MM-YYYY')"
    ex = corregir((str(input(v+' Exclusividad (Si/No)'+rojo+'*'+n+': '))).capitalize())
    while ex == "''" or (ex not in "'Si'No'"):
        print(rojo+" ERROR: Exclusividad Obligatoria")
        ex = corregir((str(input(v+' Exclusividad (Si/No)'+rojo+'*'+n+': '))).capitalize())
    atributos+=',exclusividad'
    valores+=","+ex
    vg = str(input(v+' Ventas Globales'+n+': '))
    while (vg != '' and (es_un_int(vg)==0 or int(vg)<0)):
        print(rojo+" ERROR: Rating invalido")
        vg = str(input(v+' Ventas Globales'+n+': '))
    if vg != '':
        atributos+=',ventas_globales'
        valores+=","+vg
    rtg = str(input(v+' Rating'+n+': '))
    while (rtg != '' and (es_un_int(rtg)==0 or int(rtg) not in [0,1,2,3,4,5,6,7,8,9,10])):
        print(rojo+" ERROR: Rating invalido")
        rtg = str(input(v+' Rating'+n+': '))
    if rtg != '':
        atributos+=',rating'
        valores+=","+rtg
    while True:
        try:
            cur.execute('INSERT INTO nintendo('+atributos+',fecha_estreno) VALUES('+valores+fe+')')
            break
        except Exception:
            print(rojo+" ERROR: Fecha invalida"+n)
            fe = str(input(v+' Fecha de estreno (DD-MM-YYYY)'+n+': '))
            fe = ",TO_DATE('"+fe+"','DD-MM-YYYY')"    
    atributos = 'id,nombre'
    valores = '0'+nombre
    precio = str(input(v+' Precio'+rojo+'*'+n+': '))
    while (precio == '' or es_un_int(precio)==0 or int(precio)<0):
        print(rojo+" ERROR: Precio invalido")
        precio = str(input(v+' Precio'+rojo+'*'+n+': '))
    atributos+=',precio'
    valores+=","+precio
    stock = str(input(v+' Stock'+n+': '))
    while (stock != '' and (es_un_int(stock)==0 or int(stock)<0)):
        print(rojo+" ERROR: Stock invalido")
        stock = str(input(v+' Stock'+n+': '))
    if stock != '':
        atributos+=',stock'
        valores+=","+stock
    bodega = str(input(v+' En Bodega'+n+': '))
    while (bodega != '' and (es_un_int(bodega)==0 or int(bodega)<0)):
        print(rojo+" ERROR: Cantidad en Bodega invalida")
        bodega = str(input(v+' En Bodega'+n+': '))
    if bodega != '':
        atributos+=',en_bodega'
        valores+=","+bodega
    vendidos = str(input(v+' Vendidos'+n+': '))
    while (vendidos!= '' and (es_un_int(vendidos)==0 or int(vendidos)<0)):
        print(rojo+" ERROR: Cantidad de Vendidos invalida")
        vendidos = str(input(v+' Vendidos'+n+': '))
    if vendidos != '':
        atributos+=',vendidos'
        valores+=","+vendidos
                
    cur.execute('INSERT INTO sansanoplay('+atributos+') VALUES('+valores+')')
    conn.commit()
    print(v+"\n  JUEGO AGREGADO EXITOSAMENTE"+n)
    cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.nombre = "+nombre[1:])
    for i in cur:
        print(amarillo+"\n ID"+n+": "+str(i[0]))
        print(amarillo+" Nombre"+n+": "+i[1]+amarillo+"\n Genero"+n+": "+i[2])
        print(amarillo+" Desarrollador"+n+": "+i[3]+amarillo+"\n Pubilicador"+n+": "+i[4]+amarillo+"\n Lanzamiento"+n+": "+str(i[5]).split()[0])
        print(amarillo+" Exclusividad"+n+": "+i[6]+amarillo+"\n Ventas Globales"+n+": "+str(i[7])+amarillo+"\n Rating"+n+": "+str(i[8]))
        print(amarillo+" Precio"+n+": "+str(i[11])+amarillo+"\n Stock"+n+": "+str(i[12])+amarillo+"\n Bodega"+n+": "+str(i[13]))
        print(amarillo+" Vendidos"+n+": "+str(i[14]))
    input(morado+'\n  [Enter para continuar]')



def READ():
        print()
        print(amarillo+"                  -> BUSQUEDA DE DATOS <-\n")

        print(cyan+    "             -> Elija un filtro de busqueda <-\n")

        print(cyan+"  1 "+n+"- Nombre             "+cyan+"2 "+n+"- ID                "+cyan+"3 "+n+"- Precio")
        print(cyan+"  4 "+n+"- stock              "+cyan+"5 "+n+"- Cant.Bodega       "+cyan+"6 "+n+"- Cant.Vendidos")
        print(cyan+"  7 "+n+"- Genero             "+cyan+"8 "+n+"- Desarrollador     "+cyan+"9 "+n+"- Publicador")
        print(cyan+" 10 "+n+"- Exclusividad      "+cyan+"11 "+n+"- Lanzamiento      "+cyan+"12 "+n+"- Cant.Ventas")
        print(cyan+" 13 "+n+"- rating            "+cyan+"14 "+n+"- Todos")

        tabla = " {0} | "+v+"{1}"+n+" | {2} | "+v+"{3}"+n+" | {4} | "+v+"{5}"+n+" | {6} | "+v+"{7}"+n+" | {8} | "+v+"{9}"+n+" | {10} | "+v+"{11}"+n+" | {12}"


        opcion = input(cyan + "\n Ingrese opcion: "+n)
        while (opcion == '' or int(opcion) < 1 or int(opcion) > 14):
                print(rojo + "\n  ERROR: Opcion Invalida"+n)
                opcion = input(cyan+"\n Ingrese opcion valida: "+n)

        opcion = int(opcion)
        if (opcion == 1):
                nombre_local = input(cyan+"\n Ingrese Nombre: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.nombre = '"+nombre_local+"';")
        elif (opcion == 2):
                id_local = input(cyan+"\n Ingrese ID: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.id = "+id_local+";")
        elif (opcion == 3):
                precio_local = input(cyan+"\n Ingrese Precio: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.precio = "+precio_local+";")
        elif (opcion == 4):
                stock_local	= input(cyan+"\n Ingrese Stock: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.stock = "+stock_local+";")
        elif (opcion == 5):
                bodega_local = input(cyan+"\n Ingrese Cant. en Bodega: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.en_bodega = "+bodega_local+";")
        elif (opcion == 6):
                vendidos_local = input(cyan+"\n Ingrese Vendidos Localmente: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.vendidos = "+vendidos_local+";")
        elif (opcion == 7):
                genero_local = input(cyan+"\n Ingrese Genero: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE n.genero = '"+genero_local+"';")
        elif (opcion == 8):
                desarrolladores_local = input(cyan+"\n Ingrese Desarrollador: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE n.desarrollador = '"+desarrolladores_local+"';")
        elif (opcion == 9):
                publicadoras_local = input(cyan+"\n Ingrese Publicador: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE n.publicador = '"+publicadoras_local+"';")
        elif (opcion == 10):
                exclusividad_local = input(cyan+"\n Ingrese Exclusividad (Si/No): "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE n.exclusividad = '"+exclusividad_local+"';")
        elif (opcion == 11):
                publicacion_local = "TO_DATE('"+input(cyan+"\n Ingrese Fecha: "+n)+"','MONTH DD, YYYY','NLS_DATE_LANGUAGE = AMERICAN')"
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE n.fecha_estreno = "+publicacion_local+";")
        elif (opcion == 12):
                ventas_globales_local = input(cyan+"\n Ingrese Ventas Globales: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE n.ventas_globales = "+ventas_globales_local+";")
        elif (opcion == 13):
                rating_local = input(cyan+"\n Ingrese Rating: "+n)
                cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE n.rating = "+rating_local+";")
        else:
            cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre;")

        print()


        print(tabla.format('ID','Nombre','Genero','Desarrollador','Publicador','Lanzamiento','Exclusividad','ventas globales','Rating','Precio','Stock','Bodega','Vendidos'))
        for i in cur:
                print(tabla.format(i[0],i[1],i[2],i[3],i[4],str(i[5]).split()[0],i[6],i[7],i[8],i[11],i[12],i[13],i[14]))
                        
        input(morado + '\n [Enter para continuar]')

cur.execute('''
CREATE OR REPLACE TRIGGER trg_before_delete_ID
BEFORE DELETE
ON sansanoplay
FOR EACH ROW
BEGIN
DELETE
FROM nintendo
WHERE id = :old.id;
END;
    ''')

def DELETE():
    print(amarillo+"                  -> BORRA DE DATOS <-\n")
    print(cyan+"             -> Elija un filtro de busqueda <-\n")
    print(cyan+"  1 "+n+"- Nombre             "+cyan+"2 "+n+"- ID                "+n)
    opcion = input(cyan + "\n Ingrese opcion: "+n)
    while (opcion == '' or int(opcion) < 1 or int(opcion) > 2):
        print(rojo + "\n  ERROR: Opcion Invalida"+n)
        opcion = input(cyan+"\n Ingrese opcion valida: "+n)
    opcion = int(opcion)
    if (opcion == 1):
        k = 0
        while k == 0 :
            nombre_local = corregir(input(cyan+"\n Ingrese Nombre: "+n))
            cur.execute("SELECT * FROM sansanoplay WHERE nombre ="+nombre_local)
            for i in cur:
                k=1
            if k ==0:
                print(rojo+" Nombre Invalido"+n)
        cur.execute("DELETE FROM sansanoplay WHERE nombre = "+ nombre_local+";")
    else:
        k = 0
        while k == 0:
            id_local = str(input(cyan+"\n Ingrese ID: "+n))
            while es_un_int(id_local) == 0 :
                print(rojo+" ID invalido")
                id_local = str(input(cyan+"\n Ingrese ID valido: "+n))
            cur.execute("SELECT * FROM sansanoplay WHERE id ="+id_local)
            for i in cur:
                k=1
            if k ==0:
                print(rojo+" No existe el ID"+n)
        cur.execute("DELETE FROM sansanoplay WHERE id = "+ id_local+";")
    print(v+"\n  DATO ELIMINADO EXITOSAMENTE"+n)
    input(morado+"\n  [ENTER para continuar]"+n)
    conn.commit()

cur.execute('''
CREATE OR REPLACE TRIGGER update_sansanoplay
BEFORE UPDATE ON sansanoPLAY
FOR EACH ROW
BEGIN
    IF (:new.vendidos > 0) THEN ----Actualizar stock y bodega en caso de venta
        
        IF (:new.stock - :new.vendidos) < 0 THEN   ---- No alcanza el stock
            
            IF (:new.stock + :new.en_bodega - :new.vendidos) <0 THEN  ---- no alcanza stock+bodega
                :new.vendidos:=0;  ----NO SE REALIZA LA VENTA
            ELSE ---Alcanza el stock+bodega
                :new.en_bodega := :new.en_bodega -(:new.vendidos - :new.stock);  
                :new.stock := 0;
            END IF;
            
        ELSE ---- Alcanza el stock
            :new.stock:=:new.stock - :new.vendidos;
        END IF;
    
    ELSIF (:new.vendidos < 0) THEN ----Actualizo stock en caso de devolucion
        :new.stock:=:new.stock - :new.vendidos;
    END IF;
    
    IF :new.vendidos <> 0 THEN ----Actualizar ventas globales en caso de venta efectiva
        UPDATE nintendo SET ventas_globales = :new.vendidos WHERE id = :new.id;
    END IF;
    
    IF (:new.vendidos+:old.vendidos) > 0 THEN ---actualizo vendidos en caso de venta
        :new.vendidos:= :old.vendidos + :new.vendidos;
    ELSIF (:new.vendidos+:old.vendidos) <= 0 THEN 
        :new.vendidos := 0;
    END IF;
    
    IF (:new.stock < 10) AND (:new.en_bodega > 0) THEN ---- Actualizar bodega en caso stock<10
        IF (:new.en_bodega > 10-:new.stock) THEN ---- hay suficiente en bodega para stock = 10
            :new.en_bodega := :new.en_bodega - (10-:new.stock);
            :new.stock := 10;
        ELSE   --- no hay suficiente en bodega para stock=10
            :new.stock := :new.stock + :new.en_bodega;
            :new.en_bodega := 0;
        END IF;
    END IF;
    IF :new.nombre <> :old.nombre THEN
        UPDATE nintendo SET nombre = :new.nombre, ventas_globales = 0 WHERE id = :new.id;
    END IF;
END;
''')

cur.execute('''
CREATE OR REPLACE TRIGGER update_nintendo
BEFORE UPDATE ON nintendo
FOR EACH ROW
BEGIN
    IF(:new.ventas_globales <> 0) THEN
        :new.ventas_globales := :old.ventas_globales + :new.ventas_globales;
    ELSE 
        :new.ventas_globales := :old.ventas_globales;
    END IF;
END;
''')

def UPDATE():
    print(amarillo+"\n                  -> ACTUALIZAR DATOS <-\n"+n)
    i=0
    while i == 0:
        ID = str(input(cyan+" Ingrese ID del juego"+n+": "))
        cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.id = "+ID+";")
        for i in cur:
            print(amarillo+"\n Nombre"+n+": "+i[1]+amarillo+"\n Genero"+n+": "+i[2])
            print(amarillo+" Desarrollador"+n+": "+i[3]+amarillo+"\n Pubilicador"+n+": "+i[4]+amarillo+"\n Lanzamiento"+n+": "+str(i[5]).split()[0])
            print(amarillo+" Exclusividad"+n+": "+i[6]+amarillo+"\n Ventas Globales"+n+": "+str(i[7])+amarillo+"\n Rating"+n+": "+str(i[8]))
            print(amarillo+" Precio"+n+": "+str(i[11])+amarillo+"\n Stock"+n+": "+str(i[12])+amarillo+"\n Bodega"+n+": "+str(i[13]))
            print(amarillo+" Vendidos"+n+": "+str(i[14]))
            i=1
        if i == 0:
            print(rojo+" ERROR: ID invalido"+n)
    
    print(cyan+"\n  ->"+n+" Ingrese los Nuevos Parametros.")
    print(cyan+"  ->"+n+" Si "+cyan+"No desea actualizar"+n+" el parametro, presione"+morado+" [ENTER]"+n+" para omitirlo.")
    
    input(morado+"\n  [ENTER para continuar]"+n)
    sansano = []
    nintendo = []
    x = corregir(str(input (cyan+"\n Nuevo Nombre"+n+": ")))
    while len(x)>102:
        print(rojo+" ERROR: Nombre invalido"+n)
        x = corregir(str(input (cyan+"\n Nuevo Nombre"+n+": ")))
    if x != "''":
        sansano.append("nombre = "+ x)
    x = corregir(str(input (cyan+"\n Nuevo Genero"+n+": ")))
    while len(x)>52:
        print(rojo+" ERROR: Genero invalido"+n)
        x = corregir(str(input (cyan+"\n Nuevo Genero"+n+": ")))
    if x != "''":
        nintendo.append("genero = "+ x)
    x = corregir(str(input (cyan+"\n Nuevo Desarrollador"+n+": ")))
    while len(x)>52:
        print(rojo+" ERROR: Desarrollador invalido"+n)
        x = corregir(str(input (cyan+"\n Nuevo Desarrollador"+n+": ")))
    if x != "''":
        nintendo.append("desarrollador = "+ x)
    x = corregir(str(input (cyan+"\n Nuevo Publicador"+n+": ")))
    while len(x)>52:
        print(rojo+" ERROR: Publicador invalido"+n)
        x = corregir(str(input (cyan+"\n Nuevo Publicador"+n+": ")))
    if x != "''":
        nintendo.append("publicador = "+ x)
    x = corregir(str(input (cyan+"\n Nuevo Lanzamiento (MONTH DD, YYYY)"+n+": ")))
    if x != "''":
        nintendo.append("fecha_estreno = "+ x)
    x = corregir(str(input (cyan+"\n Nueva Exclusividad"+n+": ")))
    if x != "''":
        nintendo.append("exclusividad = "+ x)
    x = str(input (cyan+"\n Nuevas Ventas Globales"+n+": "))
    while (x != '' and (es_un_int(x)==0 or int(x)<0)):
        print(rojo+" Cantidad invalida")
        x=str(input(cyan+" Ingrese Ventas Globales validas"+n+": "))
    if x != '':
        nintendo.append("ventas_globales = "+ x)
    else:
        nintendo.append("ventas_globales = 0")
    x = str(input (cyan+"\n Nuevo Rating"+n+": "))
    while (x != '' and (es_un_int(x)==0  or int(x) not in [0,1,2,3,4,5,6,7,8,9,10] )):
        print(rojo+" Rating invalido")
        x=str(input(cyan+" Ingrese Rating valido"+n+": "))
    if x != '':
        nintendo.append("rating = "+ x)
    x = str(input (cyan+"\n Nuevo Precio"+n+": "))
    while (x != '' and (es_un_int(x)==0 or int(x)<0)):
        print(rojo+" Precio invalido")
        x=str(input(cyan+" Ingrese Precio valido"+n+": "))
    if x != '':
        sansano.append("precio = "+ x)
    x = str(input (cyan+"\n Nuevo Stock"+n+": "))
    while (x != '' and (es_un_int(x)==0 or int(x)<0)):
        print(rojo+" Stock invalido")
        x=str(input(cyan+" Ingrese Stock valido"+n+": "))
    if x != '':
        sansano.append("stock = "+ x)
    x = str(input (cyan+"\n Nueva Bodega"+n+": "))
    while (x != '' and (es_un_int(x)==0 or int(x)<0)):
        print(rojo+" Cantidad invalida")
        x=str(input(cyan+" Ingrese Cantidad en Bodega valida"+n+": "))
    if x != '':
        sansano.append("en_bodega = "+ x)

    cn = ','.join(nintendo)
    cs = ','.join(sansano)

    if cn != '':
        cur.execute("UPDATE nintendo SET "+cn+" WHERE id = "+str(ID))
    if cs != '':
        cur.execute("UPDATE sansanoplay SET "+cs+" WHERE id = "+str(ID))
    cur.execute("SELECT * FROM nintendo n INNER JOIN sansanoplay s ON n.id = s.id AND n.nombre = s.nombre WHERE s.id = "+ID+";")
    print(v+"\n Datos Actualizados exitosamente.")
    for i in cur:
        print(amarillo+"\n Nombre"+n+": "+i[1]+amarillo+"\n Genero"+n+": "+i[2])
        print(amarillo+" Desarrollador"+n+": "+i[3]+amarillo+"\n Pubilicador"+n+": "+i[4]+amarillo+"\n Lanzamiento"+n+": "+str(i[5]).split()[0])
        print(amarillo+" Exclusividad"+n+": "+i[6]+amarillo+"\n Ventas Globales"+n+": "+str(i[7])+amarillo+"\n Rating"+n+": "+str(i[8]))
        print(amarillo+" Precio"+n+": "+str(i[11])+amarillo+"\n Stock"+n+": "+str(i[12])+amarillo+"\n Bodega"+n+": "+str(i[13]))
        print(amarillo+" Vendidos"+n+": "+str(i[14]))
        
    input(morado+"\n  [ENTER para continuar]"+n)
    conn.commit()

'''-----------------------------------------------------------'''

def ventas_devolucion(i):
    if i == 1:
        print(amarillo+"\n      -> VENTA DE JUEGO <-")
    else:
        print(amarillo+"\n    -> DEVOLUCION DE JUEGO <-")
    while True:
        try:
            k=0
            while k == 0:
                ID = str(input(cyan+"\n Ingrese ID del juego"+n+": "))
                cur.execute("SELECT vendidos FROM sansanoplay WHERE id = "+ID+";")
                for x in cur:
                    old_ventas = int(x[0])
                    k=1
                if k == 0:
                    print(rojo+" ERROR: ID invalido"+n)
            if i == 1:
                cantidad = int(input(cyan+"\n Ingrese Cantidad de Venta"+n+": "))
            else:
                cantidad = -(int(input(cyan+"\n Ingrese Cantidad de Devolucion"+n+": ")))
            cur.execute("UPDATE sansanoplay SET vendidos = "+str(cantidad)+" WHERE id = "+ID+";")
            cur.execute("SELECT vendidos, en_bodega, stock FROM sansanoplay WHERE id = "+ID+";")
            for x in cur:
                new_ventas = int(x[0])
                bodega = int(x[1])
                stock = int(x[2])
            if (new_ventas == old_ventas):
                print(rojo+"\n  No hay productos suficientes para realizar la venta"+n)
                print("  La cantidad total de productos en la tienda es de " +v+ str(bodega+stock)+n)
            else:
                if i == 1:
                    print(v+"\n LA VENTA SE HA REALIZADO EXITOSAMENTE")
                else:
                    print(v+"\n LA DEVOLUCION SE HA REALIZADO EXITOSAMENTE")
            conn.commit()
            input(morado+"\n  [ENTER para continuar]"+n)
            break
        except Exception:
            print(rojo+" ERROR: Intentelo nuevamente"+n)

'''-----------------------------------------------------------'''

def borrar():
    cur.execute("DROP TABLE sansanoplay")
    cur.execute("DROP TABLE nintendo;")
    cur.execute("DROP SEQUENCE secu;")
    cur.execute("DROP VIEW top_3_desloc;")
    cur.execute("DROP VIEW top_3_genloc;")
    cur.execute("DROP VIEW top_3_genglob;")
    cur.execute("DROP VIEW top_5_ex;")
    cur.execute("DROP VIEW top_rait;")
    conn.commit()
    print(v+"\n LA BASE DE DATOS HA SIDO BORRADA EXITOSAMENTE")
    input(morado+"\n  [ENTER para continuar]"+n)
    

def MENU():
    print ()
    print (cyan+"        -> Escoja accion a realizar <-"+n)
    print ()
    print (cyan+"  1 "+n+"- Agregar Juego                "+cyan+"2 "+n+"- Leer Datos")
    print (cyan+"  3 "+n+"- Actualizar Datos             "+cyan+"4 "+n+"- Borrar Juego")
    print (cyan+"  5 "+n+"- Realizar Venta               "+cyan+"6 "+n+"- Realizar Devolucion")
    print ()
    print (cyan+"  -> Consultar:")
    print ()
    print (v+"    7 "+n+"- 5 Juegos exclusivos mas caros")
    print (v+"    8 "+n+"- 3 Generos mas vendidos localmente")
    print (v+"    9 "+n+"- 3 Generos mas vendidos globalmente")
    print (v+"   10 "+n+"- 3 Desarrolladoras con mas ventas")
    print (v+"   11 "+n+"- Juegos con mejor rating")
    print (rojo+"\n   12 - BORRAR BASE DE DATOS")
    print ()
    print (rojo+" 13 "+n+"- Salir de la base de datos")
    
    opcion = input(cyan+"\n Ingrese opcion deseada: "+n)
    while (opcion == '' or int(opcion) < 1 or int(opcion) > 13):
        print (rojo+"\n ERROR: Opcion invalida"+n)
        print()
        opcion = input(cyan+"Ingrese opcion valida: "+n)
    return int(opcion)


'''----------------------------------------------------------------'''


print (amarillo+"       -> Base de Datos SansanoPlay <-")
print ()
print (v+"       Se ha cargado la base de datos "+n)
print ()

opcion = MENU()


while (opcion != 13):

	#Insertar
	if (opcion == 1):
		insert_new()

	#Recuperar
	elif (opcion == 2):
		READ()

	#Actualizar
	elif (opcion == 3):
		UPDATE()

	#Borrar
	elif (opcion == 4):
		DELETE()

        #VENTA
	elif (opcion == 5):
		ventas_devolucion(1)

	#DEVOLUCION
	elif (opcion == 6):
		ventas_devolucion(0)

	#Consultar exclusivos mas caros
	elif (opcion == 7):
		top_5_ex()

	#Consultar generos mas vendidos localmente
	elif (opcion == 8):
		top_3_genloc()

	#Consultar generos mas vendidos globalmente
	elif (opcion == 9):
		top_3_genglob()

	#Consultar desarrolladoras con mas ventas
	elif (opcion == 10):
		top_3_desloc()

	#Listar juegos con mejor rating por fecha
	elif (opcion == 11):
		top_rait()

	#Borrar BD
	elif (opcion == 12):
		borrar()
		break
	opcion=MENU()

cur.close()
conn.close()
