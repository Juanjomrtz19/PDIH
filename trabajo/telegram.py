import requests
from meses import meses, meses_numero
from datetime import datetime, timedelta
from telepot.loop import MessageLoop
import telepot
import time
import random
from conexion import cursor, conexion
import signal
import sys
from letras_horas import horas_mysql,expresiones_horas,mensaje_comandos
import os



def comprobar_hora(hora):
    hora = datetime.datetime.strptime(hora, '%H:%M:%S').time()
    esta_en_rango = [True]
    if (hora >= datetime.time(21, 0) and hora < datetime.time(9, 0)) or (hora >= datetime.time(14,0) and hora < datetime.time(16, 30)):
        msg = "Lo siento pero la Clínica esta cerrada de 9 de la noche a 9 de la mañana y de  2 de la tarde a 4 y media de la tarde"
        esta_en_rango.append(msg)
        esta_en_rango[0] = False
    return esta_en_rango

def signal_handler(sig, frame):
    conexion.commit()
    cursor.close()
    conexion.close()
    print('Programa detenido por usuario')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

def aniadirUsuario(nombre, chat_id):
    sql = "INSERT INTO Usuario(chat_id, user) VALUES (%s,%s)"
    cursor.execute(sql, (nombre, chat_id))
    conexion.commit()

def estaUsuario(nombre, id):
    sql = "SELECT * FROM Usuario WHERE chat_id=%s AND user=%s"
    cursor.execute(sql, (id,nombre))
    if len(cursor.fetchall()) == 0:
        print(cursor.fetchall())
        return False
    else:
        return True

def citaDisponible(fecha, hora):
    sql = "SELECT fecha FROM Cita WHERE fecha=%s AND hora=%s"
    cursor.execute(sql,(fecha,hora))
    datos = cursor.fetchall()
    if len(datos) == 0:
        return True
    else:
        return False
    
def citaOcupadaUsuario(fecha, usuario):
    sql = "SELECT fecha FROM Cita WHERE (fecha=%s) AND (usuario=%s)"
    cursor.execute(sql,(fecha,usuario))
    datos = cursor.fetchall()
    if len(datos) == 0:
        return False
    else:
        return True

def handle(msg):
    #DATOS UTILES DEL CHAT
    chat_id = msg['chat']['id']
    command = msg['text'].upper()
    nombre = msg['from']['first_name']
    nickname = msg['from']['username']
    
    #COMANDOS
    if command == "/START":
        bot.sendMessage(chat_id, 'Hola bienvenido soy el asistente de la clínica Dentista Artemai si necesita consultar horarios libres, pedir cita, cancelar cita soy perfecto para ti, para ver los comandos disponibles pon /comandos')

    elif command == "/TIME":
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

    elif command == "/CONSULTARCITAS":
        sql ="SELECT fecha,hora FROM Cita WHERE usuario = %s"
        cursor.execute(sql,(nickname,))
        datos = cursor.fetchall()
        print(datos)
        
        if(len(datos) == 0):
            mensaje = "Lo siento no hay ninguna cita reservada a su nombre"
        else:
            mensaje = "Estas son sus citas: \n "
            
            for dato in datos:
                #lista_fecha = dato[0].split('-')
                hora = str(dato[1])
                fecha = str(dato[0])
                print(fecha)
                lista_fecha = fecha.split('-')
                mensaje = mensaje + "- El día " + lista_fecha[2] + " de " + meses[lista_fecha[1]] + " del año " + lista_fecha[0] + " " + expresiones_horas[hora] + "\n"
        
        bot.sendMessage(chat_id, mensaje)

    elif command.find("/INSERTARCITA") != -1:
        if(estaUsuario(nickname, chat_id) == False):
            print("ENTROOOOOO")
            aniadirUsuario(chat_id, nickname)

        mensaje = command.split(" ")
        print(len(mensaje))
        if(len(mensaje) == 1):
            bot.sendMessage(chat_id, "Ha olvidado escribir el día y la fecha al lado, \n P.Ejemplo: /insertarcita el 19 de mayo de 2001 a las seis de la tarde")
        elif len(mensaje) != 13 and len(mensaje) != 15:
            bot.sendMessage(chat_id, "El formato que ha introducido es incorrecto, el formato correcto es el DD de (mes escrito en texto) de YYYY a las (hora en letra) de la (parte del día que desee)")

        else:
            if len(mensaje) == 13:
                if(len(mensaje[2]) == 1):
                    mensaje[2] = '0' + mensaje[2]
                fecha = mensaje[6] + '-' + meses_numero[mensaje[4]] + '-' + mensaje[2]
                formato_hora = mensaje[7] + " " + mensaje[8] + " " + mensaje[9] + " " + mensaje[10] + " " + mensaje [11] + " " + mensaje[12]
                formato_hora = formato_hora.lower()
                print(formato_hora)
            else:
                if(len(mensaje[2]) == 1):
                    mensaje[2] = '0' + mensaje[2]
                fecha = mensaje[6] + '-' + meses_numero[mensaje[4]] + '-' + mensaje[2]
                formato_hora = mensaje[7] + " " + mensaje[8] + " " + mensaje[9] + " " + mensaje[10] + " " + mensaje [11] + " " + mensaje[12] + " " + mensaje[13] + " " + mensaje[14]
                formato_hora = formato_hora.lower()
                print(formato_hora)
            try:
                hora = horas_mysql[formato_hora]
            except:
                bot.sendMessage(chat_id, "Ha ocurrido un error el formato recuerde ingresar su cita como en este ejemplo: el 7 de abril de 2024 a las cinco de la tarde y recuerde que los saltos se dan de media hora en media hora por ejemplo a las cinco, a las cinco y media, a las seis,... esto se debe a que de tiempo a atender correctamente a todos los clientes")
            comprobacion = comprobar_hora(hora)
            print(hora)
            print(comprobacion)

            if len(comprobacion) == 2:
                bot.sendMessage(chat_id, comprobacion[1])
            else:
                sql = "INSERT INTO Cita(usuario,fecha,hora) VALUES(%s, %s, %s)"

                if(citaDisponible(fecha, hora)):
                    try:
                        cursor.execute(sql,(nickname, fecha, hora))
                        
                        bot.sendMessage(chat_id, "La cita ha sido ingresada con éxito")
                    except:
                        bot.sendMessage(chat_id, "Lo siento ha ocurrido algún error, seguramente sea que ha intentado insertar una fecha que es anterior a la actual")
                else:
                    bot.sendMessage(chat_id, "Ese día y a esa hora ya esta ocupada")

    

    elif command.find("/CANCELARCITA") != -1:
        mensaje = command.split(" ")
        if(len(mensaje) == 1):
            bot.sendMessage(chat_id, "Ha olvidado escribir el día y la fecha al lado, \n P.Ejemplo: /cancelarcita el 19 de mayo de 2001 a las  cinco de la tarde")
        elif(len(mensaje) != 13 and len(mensaje) != 15):
            bot.sendMessage(chat_id, "El formato que ha introducido es incorrecto, el formato correcto es el DD de (mes escrito en texto) de YYYY a las (hora en letra) de la tarde/mañana")
        else:
            if len(mensaje) == 13:
                if(len(mensaje[2]) == 1):
                    mensaje[2] = '0' + mensaje[2]
                fecha = mensaje[6] + '-' + meses_numero[mensaje[4]] + '-' + mensaje[2]
                formato_hora = mensaje[7] + " " + mensaje[8] + " " + mensaje[9] + " " + mensaje[10] + " " + mensaje [11] + " " + mensaje[12]
                formato_hora = formato_hora.lower()
            else:
                if(len(mensaje[2]) == 1):
                    mensaje[2] = '0' + mensaje[2]
                fecha = mensaje[6] + '-' + meses_numero[mensaje[4]] + '-' + mensaje[2]
                formato_hora = mensaje[7] + " " + mensaje[8] + " " + mensaje[9] + " " + mensaje[10] + " " + mensaje [11] + " " + mensaje[12]+ " " + mensaje[13] + " " + mensaje[14]
                formato_hora = formato_hora.lower()
                
            print(formato_hora)
            try:
                hora = horas_mysql[formato_hora]
                
            except:
                bot.sendMessage(chat_id, "Ha ocurrido un error el formato recuerde ingresar su cita como en este ejemplo: el 7 de abril de 2024 a las cinco de la tarde y recuerde que los saltos se dan de media hora en media hora por ejemplo a las cinco, a las cinco y media, a las seis,... esto se debe a que de tiempo a atender correctamente a todos los clientes")
            comprobacion = comprobar_hora(hora)

            if len(comprobacion) == 2:
                bot.sendMessage(chat_id, comprobacion[1])
            else:
                sql = "DELETE FROM Cita WHERE fecha=%s AND usuario=%s AND hora=%s"
                if(citaOcupadaUsuario(fecha, nickname)):
                    try:
                        cursor.execute(sql, (fecha, nickname, hora))
                        bot.sendMessage(chat_id, "Cita borrada con éxito")        
                    except:
                        bot.sendMessage(chat_id, "Ha ocurrido un error y no se ha podido borrar la cita")
                else:
                    bot.sendMessage(chat_id, "No tiene ninguna cita ese día")
    elif command == "/COMANDOS":
        bot.sendMessage(chat_id, mensaje_comandos)

    #FRASES COLOQUIALES
    elif command.find("CONSULTAR UNA CITA")!=-1 or command.find("CONSULTAR")!=-1:
        bot.sendMessage(chat_id, "Para consultar una cita introduzca el comando /consultarcitas")
    elif command=="HOLA":
        bot.sendMessage(chat_id, 'Hola {} si necesitas mas información pon /start'.format(nombre))
    elif command.find("NÚMERO DE TELÉFONO")!= -1 or command.find("MÓVIL")!=-1 or command.find("NÚMERO")!=-1 or command.find("MOVIL")!=-1 or command.find("TELÉFONO")!=-1 or command.find("NUMERO")!=-1:
        bot.sendMessage(chat_id, "El número de teléfono por si quieres obtener aun más información o discriminas a los bots y por eso no quieres hablar conmigo es 673246236")
    elif command.find("CHISTE") != -1:
        num = random.randint(1, 80)
        print(num)
        sql="SELECT mensaje FROM Chiste WHERE id=%s"
        cursor.execute(sql, (num,))
        mensaje = cursor.fetchall()
        bot.sendMessage(chat_id, mensaje[0][0])

    else:
        bot.sendMessage(chat_id, "Lo siento no he entendido el mensaje envíeme otro a ver si lo entiendo, para mirar los comandos disponibles introduzca /comandos")    

bot = telepot.Bot(os.environ.get('API_KEY'))

MessageLoop(bot, handle).run_as_thread()
print('Bot ready')



while 1:
    time.sleep(10)

