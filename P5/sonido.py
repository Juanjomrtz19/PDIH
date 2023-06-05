import pygame
import numpy as np
import matplotlib.pyplot as plt
import wave
from scipy import signal
import audioop


#LEER Y REPRODUCIR FICHEROS
pygame.init()

archivo1 = "/home/juanjo/4aniocarrera/SEGUNDO_CUATRI/PDIH NO GIT/PDIH/P5/nombre.wav"
archivo2 = "/home/juanjo/4aniocarrera/SEGUNDO_CUATRI/PDIH NO GIT/PDIH/P5/apellidos.wav"

pygame.mixer.init()

nombre = pygame.mixer.Sound(archivo1)
apellidos = pygame.mixer.Sound(archivo2)


nombre.play()
pygame.time.wait(int(nombre.get_length() * 1000))

apellidos.play()
pygame.time.wait(int(apellidos.get_length() * 1000))

#GENERAR GRÁFICAS
array_nombre = pygame.sndarray.array(nombre)
array_apellidos = pygame.sndarray.array(apellidos)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

ax1.plot(array_nombre)
ax1.set_title('Forma de onda del nombre')

ax2.plot(array_apellidos)
ax2.set_title('Forma de onda del de los apellidos')

plt.tight_layout()
plt.show()

pygame.mixer.quit()
pygame.quit()

#OBTENER CABECERAS DE LOS SONIDOS
with wave.open(archivo1, 'rb') as sonido:
    cabecera1 = sonido.getparams()

with wave.open(archivo2, 'rb') as sonido:
    cabecera2 = sonido.getparams()

print("Información del sonido del nombre: \n {}".format(cabecera1))
print("Información del sonido de los apellidos: \n {}".format(cabecera2))



#COMBINAR SONIDOS
infiles = [archivo1, archivo2]
outfile = "sounds.wav"

data= []
for infile in infiles:
    w = wave.open(infile, 'rb')
    data.append( [w.getparams(), w.readframes(w.getnframes())] )
    w.close()

output = wave.open(outfile, 'wb')
output.setparams(data[0][0])
output.writeframes(data[0][1])
output.writeframes(data[1][1])
output.close()

#OBTENER FORMA DE ONDA
archivo = "/home/juanjo/4aniocarrera/SEGUNDO_CUATRI/PDIH NO GIT/PDIH/P5/sounds.wav"

with wave.open(archivo, 'rb') as wav:
    canales = wav.getnchannels()
    profundidad_bits = wav.getsampwidth()
    frecuencia_muestreo = wav.getframerate()
    frames = wav.getnframes()

    frames_audio = wav.readframes(frames)

audio_array = np.frombuffer(frames_audio, dtype=np.int16)

tiempo = np.linspace(0, len(audio_array) / frecuencia_muestreo, num=len(audio_array))

fig, ax = plt.subplots()
ax.plot(tiempo, audio_array)

ax.set(xlabel='Tiempo (s)', ylabel='Amplitud',
       title='Forma de la combinacion de ambos sonidos')
ax.grid()

plt.show()

#PASAR FILTRO DE FRECUENCIA
minima = 10000
maxima = 20000

frecuencia_min = minima / (frecuencia_muestreo / 2)
frecuencia_max = maxima / (frecuencia_muestreo / 2)

orden = 5
b, a = signal.butter(orden, [frecuencia_min, frecuencia_max], btype='band')

datos_filtrados = signal.lfilter(b, a, audio_array)

#GUARDAR ARCHIVO
archivo_filtrado = "mezcla.wav"
with wave.open(archivo_filtrado, 'wb') as wav_filtrado:
    wav_filtrado.setnchannels(canales)
    wav_filtrado.setsampwidth(profundidad_bits)
    wav_filtrado.setframerate(frecuencia_muestreo)
    wav_filtrado.writeframes(datos_filtrados.astype(np.int16).tobytes())
