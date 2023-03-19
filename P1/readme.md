# Documentación Práctica 1: Entrada/Salida utilizando interrupciones con lenguaje C

En esta documentación explicaré como he llevado a cabo la práctica 1 de PDIH es decir cada una de las funciones que se pedían en dicho guión.

Realizada por Juan José Martínez Águila.

# Funciones obligatorias

- gotoxy(): Esta función recibe dos parámetros, la posición x y la posición y, y a continuación desplaza el cursos hasta la posición (x,y).

Como haremos en todas las funciones a partir de ahora al principio de cada función crearemos dos variables de tipo **union REGS** denominadas **inregs** y **outregs**.

En **inregs** el registro **dl** igualaremos al valor de la **x**, el registro dh igualaremos al valor de la **y**, el registro **bh** igualaremos a 0 y por último el registro **ah** lo igualaremos a 0x02. Por último llamaramemos a la función **int86** con número de interrupción 0x010. 
![this is a image](/P1/img/1.png)


