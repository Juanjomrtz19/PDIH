horas_mysql = {
    'a las nueve de la mañana': '09:00:00',
    'a las nueve y media de la mañana': '09:30:00',
    'a las diez de la mañana': '10:00:00',
    'a las diez y media de la mañana': '10:30:00',
    'a las once de la mañana': '11:00:00',
    'a las once y media de la mañana': '11:30:00',
    'a las doce de la mañana': '12:00:00',
    'a las doce y media de la mañana': '12:30:00',
    'a la una de la tarde': '13:00:00',
    'a la una y media de la tarde': '13:30:00',
    'a las dos de la tarde': '14:00:00',
    'a las dos y media de la tarde': '14:30:00',
    'a las tres de la tarde': '15:00:00',
    'a las tres y media de la tarde': '15:30:00',
    'a las cuatro de la tarde': '16:00:00',
    'a las cuatro y media de la tarde': '16:30:00',
    'a las cinco de la tarde': '17:00:00',
    'a las cinco y media de la tarde': '17:30:00',
    'a las seis de la tarde': '18:00:00',
    'a las seis y media de la tarde': '18:30:00',
    'a las siete de la tarde': '19:00:00',
    'a las siete y media de la tarde': '19:30:00',
    'a las ocho de la noche': '20:00:00',
    'a las ocho y media de la noche': '20:30:00',
    'a las nueve de la noche': '21:00:00',
    'a las nueve y media de la noche': '21:30:00',
    'a las diez de la noche': '22:00:00'
}


import datetime

def crear_diccionario_expresiones_horas():
    diccionario_expresiones = {}
    hora = datetime.datetime(2023, 1, 1, 9, 0, 0)
    while hora.time() <= datetime.time(22, 0, 0):
        hora_mysql = hora.strftime("%H:%M:%S")
        expresion_hora = ""
        if hora.hour == 0 and hora.minute == 0:
            expresion_hora = "a la medianoche"
        elif hora.hour == 12 and hora.minute == 0:
            expresion_hora = "al mediodía"
        elif hora.minute == 0:
            expresion_hora = "a las " + hora.strftime("%I %p").lstrip("0").replace(" 0", " ")
        elif hora.minute == 30:
            expresion_hora = "a las " + hora.strftime("%I y media %p").lstrip("0").replace(" 0", " ")
        else:
            expresion_hora = "a las " + hora.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
        diccionario_expresiones[hora_mysql] = expresion_hora
        hora += datetime.timedelta(minutes=30)
    return diccionario_expresiones

expresiones_horas = crear_diccionario_expresiones_horas()

mensaje_comandos="""
    Estos son los comandos que puede utilizar para comunicarse conmigo: \n
    - /consultarcitas: sirve para consultar todas las citas que ha reservado \n
    - /insertarcita [fecha en el formato correcto (el 19 de mayo de 2023 a las cinco de la tarde por ejemplo)]: Sirve para reservar la cita en la fecha que vaya después del comando \n
    - /cancelarcita [fecha en el formato correcto (el 19 de mayo de 2023 a las cinco de la tarde por ejemplo)]: Cancela la cita de la fecha que vaya seguida del comando \n
    - Para obtener el número de la clínica preguntele por el número por ejemplo: ¿Me dices el número de teléfono de la clínica? \n
    - Si le dices que te cuente un chiste te lo contará
"""