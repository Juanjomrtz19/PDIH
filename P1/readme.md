# Documentación Práctica 1: Entrada/Salida utilizando interrupciones con lenguaje C

En esta documentación explicaré como he llevado a cabo la práctica 1 de PDIH es decir cada una de las funciones que se pedían en dicho guión.

Realizada por Juan José Martínez Águila.

# Funciones obligatorias

- gotoxy(): Esta función recibe dos parámetros, la posición x y la posición y, y a continuación desplaza el cursos hasta la posición (x,y).

Como haremos en todas las funciones a partir de ahora al principio de cada función crearemos dos variables de tipo **union REGS** denominadas **inregs** y **outregs**.

En **inregs** el registro **dl** igualaremos al valor de la **x**, el registro dh igualaremos al valor de la **y**, el registro **bh** igualaremos a 0 y por último el registro **ah** lo igualaremos a 0x02. Por último llamaramemos a la función **int86** con número de interrupción 0x010. 
![this is a image](/P1/img/1.png)

En la imagen podemos observar que debajo de BC esta el nuevo cursor que hemos posicionado con la función **gotoxy(3,5)**.

- setcursortype(int tipo_cursor): Esta función esta implementada mediante un switch en función del tipo del cursor que sea, el registro **ah** será en los tres distintos casos 0x01.

Si el cursor que se desea tiene el valor 0 (invisible) el registro ch valdrá 010 y el registro cl valdrá 000.

Si el cursor que se desea tiene el valor 1 (normal) el registro ch valdrá 010 y el registro cl 010.

Si el cursor que se desea tiene el valor 2 (grueso) el registro ch valdrá 000 y el registro cl valdrá 010.

Por último llamaremos a la función int86 con la interrupción 0x10.

- setvideomode(unsigned char modo): Esta función recibe un parámetro unsigned char que será el modo en que queramos ponerlo, 0x02 para modo texto y 0x04 para modo gráfico.

El registro ah valdrá 0x00 y el registro al valdrá el modo que elijamos. Por último llamaremos a la función int86 con la interrupción 0x10.

- unsigned char getvideomode(): Esta funcíon devuelve el modo de vídeo que estamos utilizando. Elregistro ah valdrá 0xF utilizamos la función int86 con la interrupción 0x10 y devolvemos el registro al de outregs.

- void textcolor(int color): Recibe el valor del color al que queremos cambiar y cambiamos el valor de la variable ctexto al valor del color pasado.

- void textbackground(int color): Recibe el valor del color al que queremos cambiar y cambiamos el valor de la variable cfondo al valor del color pasado.

- void clsrc(): Esta funcíon limpia la pantalla y esto lo llevaremos a cabo utilizando la función que hemos programado setvideomode y la cambiaremos a modo gráfico y luego a modo texto.

- cputchar(char c): Esta función imprimirá el caracter c con el color de fondo y color de texto elegido.

El registro ah valdría 0x09, el registro al valdrá c, el registro bl valdrá cfondo << 4 | ctexto, el registro bh valdrá 0x00 y el registro cx valdrá 1. Por último utilizaremos la función int86 con interrupción 0x10.

![this is a image](/P1/img/2.png)

- int mi_getche(): Esta función obtiene un carácter de teclado y lo imprime por pantalla, el registro ah valdrá 1, utilizaremos la función int86 con el número de interrupción 0x21 y devolverá el registro al de outregs.

# Funciones optativas
- void dibujarRecuadro(int x1, int y1, int x2, int y2, int colort, int colorf): En esta función primero asignamos los nuevos colores elegidos. Y a partir de las coordenadas dadas en los parámetros de la función y
ayudándonos de la funciones gotoxy para desplazarnos y cputchar para imprimir los caracteres.
![this is a image](/P1/img/3.png)

- void dibujo(): Esta función pondrá el modo gráfico y dibujará una casa con la ayuda de la función pixel.
![this is a image](/P1/img/4.png)


