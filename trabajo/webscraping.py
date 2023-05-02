import requests
from bs4 import BeautifulSoup
from conexion import conexion, cursor

def webScraping(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    contenidos = soup.find('div', id="wrap").find('div', class_='container container-main').find('div', id="display-posts").find_all('div', class_='post')
    chistes = []
    for contenido in contenidos:
        letra_chiste = contenido.a.p.get_text()
        chistes.append(letra_chiste)
    return chistes

chistes = webScraping("https://www.chistescortosbuenos.com/")
for chiste in chistes:
    sql = 'INSERT INTO Chiste(mensaje) VALUES(%s)'
    cursor.execute(sql, (chiste,))

sql = "SAVEPOINT solochistes"
cursor.execute(sql)
conexion.commit()

