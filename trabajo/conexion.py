import mysql.connector
conexion =  mysql.connector.connect(
            host='localhost', #contraseña
            port='3306', #puerto 
            user='ddsi', #usuario de mysql al que conectarse
            password='1234', #contraseña
            db='chatbot' #base de datos a la que conectarse dentro de mysql
            )

cursor = conexion.cursor(buffered=True)
    