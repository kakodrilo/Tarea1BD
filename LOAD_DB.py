import pyodbc
import random
import csv


def corregir(s):
    if ("'" in s):
        s = s.replace("'", "''")
    if ("#" in s):
        s = s.replace("#","'||'#'||'")
    return "'"+s+"'"

conn = pyodbc.connect('DSN=T1BD;UID=system;PWD=Equipo32019;CHARSET=UTF8')
cur = conn.cursor()
'''
cur.execute('DROP TABLE sansanoplay')
cur.execute('DROP TABLE nintendo')
cur.execute('DROP SEQUENCE secu')
'''
id_j = "id INT PRIMARY KEY,"
nombre = "nombre VARCHAR(100) NOT NULL CHECK(nombre<>''),"
genero = "genero VARCHAR(50),"
des = "desarrollador VARCHAR(50) NOT NULL,"
pbl = "publicador VARCHAR(50) NOT NULL,"
fe = "fecha_estreno DATE,"
ex = "exclusividad CHAR(2) NOT NULL CHECK(exclusividad='No' or exclusividad='Si'),"
vg = "ventas_globales INT DEFAULT 0 CHECK(ventas_globales>=0),"
rtg = "rating INT DEFAULT 0 CHECK(rating>=0 AND rating<=10)"

cur.execute('CREATE TABLE nintendo('+id_j+nombre+genero+des+pbl+fe+ex+vg+rtg+')')

id_j = "id INT PRIMARY KEY,"
nombre = "nombre VARCHAR(100) NOT NULL CHECK(nombre<>''),"
precio = "precio INT NOT NULL CHECK(precio>=0),"
stock = "stock INT DEFAULT 0 CHECK(stock>=0),"
bodega = "en_bodega INT DEFAULT 0 CHECK(en_bodega>=0),"
vendidos = "vendidos INT DEFAULT 0"

cur.execute('CREATE TABLE sansanoplay('+id_j+nombre+precio+stock+bodega+vendidos+')')

cur.execute('CREATE SEQUENCE secu START WITH 1')

cur.execute('''
CREATE OR REPLACE TRIGGER insert_nintendo
BEFORE INSERT ON nintendo
FOR EACH ROW
BEGIN
    SELECT secu.NEXTVAL
    INTO :new.id
    FROM dual;
END;

            ''')

cur.execute('''
CREATE OR REPLACE TRIGGER insert_sansanoplay
BEFORE INSERT ON sansanoplay
FOR EACH ROW
BEGIN
    SELECT secu.CURRVAL
    INTO :new.id
    FROM dual;
END;

            ''')

with open('Nintendo.csv','r') as FILE:
    reader = csv.reader(FILE)
    for ln in reader:
        if (ln[0] != 'id'):
            id_j = "0,"
            nombre = corregir(ln[1])+","
            genero = corregir(ln[2])+","
            des = corregir(ln[3])+","
            pbl = corregir(ln[4])+","
            if ("," not in ln[5]):
                ln[5] = ""
            fe = "TO_DATE('"+ln[5]+"','MON DD, YYYY','NLS_DATE_LANGUAGE = AMERICAN'),"
            ex = "'"+ln[6]+"',"
            vg = str(random.randint(0,16000000))+','
            rtg = str(random.randint(0,10))
            cur.execute('INSERT INTO nintendo VALUES('+id_j+nombre+genero+des+pbl+fe+ex+vg+rtg+')')
            precio = str(random.randint(5,50)*1000)+","
            stock = str(random.randint(10,50))+","
            bodega = str(random.randint(0,1000))+","
            vendidos = str(random.randint(0,1000))
            cur.execute('INSERT INTO sansanoplay VALUES('+id_j+nombre+precio+stock+bodega+vendidos+')')



conn.commit()
cur.close()
conn.close()
