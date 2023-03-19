#include <stdio.h>
#include <dos.h>

unsigned char cfondo = 0;
unsigned char ctexto = 0;

void mi_pausa(){
   union REGS inregs, outregs;
	 inregs.h.ah = 8;
	 int86(0x21, &inregs, &outregs);
}

void mi_putchar(char c){
	 union REGS inregs, outregs;

	 inregs.h.ah = 2;
	 inregs.h.dl = c;
	 int86(0x21, &inregs, &outregs);
}

void gotoxy(int x, int y){
    union REGS inregs, outregs;
    inregs.h.dl = x;
    inregs.h.dh = y;
    inregs.h.bh = 0;
    inregs.h.ah = 0x02;

    int86(0x10, &inregs, &outregs);
}

void setcursortype(int tipo_cursor){
	union REGS inregs, outregs;
	inregs.h.ah = 0x01;
	switch(tipo_cursor){
		case 0: //invisible
			inregs.h.ch = 010;
			inregs.h.cl = 000;
			break;
		case 1: //normal
			inregs.h.ch = 010;
			inregs.h.cl = 010;
			break;
		case 2: //grueso
			inregs.h.ch = 000;
			inregs.h.cl = 010;
			break;
	}
	int86(0x10, &inregs, &outregs);
}

void setvideomode(unsigned char modo){
    union REGS inregs, outregs;
    inregs.h.ah = 0x00;
    inregs.h.al = modo;
    int86(0x10, &inregs, &outregs);
}

unsigned char getvideomode(){
    union REGS inregs, outregs;
    inregs.h.ah = 0xF;
    int86(0x10, &inregs, &outregs);
    return outregs.h.al;
}

void textcolor(int color){
	/*
	union REGS inregs, outregs;
	inregs.h.ah = 0x09;
	inregs.h.al = c;
	cfondo = color;
	inregs.h.bl = cfondo << 4 | ctexto;
	inregs.h.bh = 0x00;
	inregs.x.cx = 1;
	int86(0x10, &inregs, &outregs);
	return;
	*/
	ctexto = color;
}

void textbackground(int color){
	cfondo = color;
}

void clsrc(){
	setvideomode(0x04); //MODO GRÁFICO
	setvideomode(0x02); //MODO TEXTO
}

void cputchar(char c){
	union REGS inregs, outregs;
	inregs.h.ah = 0x09;
	inregs.h.al = c;
	inregs.h.bl = cfondo << 4 | ctexto;
	inregs.h.bh = 0x00;
	inregs.x.cx = 1;
	int86(0x10, &inregs, &outregs);
	return;
}

int mi_getche(){
	 union REGS inregs, outregs;
	 int caracter;

	 inregs.h.ah = 1;
	 int86(0x21, &inregs, &outregs);

	 caracter = outregs.h.al;
	 return caracter;
}

//_________________________OPTATIVOS___________________________
void dibujarRecuadro(int x1, int y1, int x2, int y2, int colort, int colorf){
	int i;
	int j;
	textcolor(colort);
	textbackground(colorf);
	for(i=x1; i<=x2;i++){
		gotoxy(i,y1);
		cputchar('B');
		gotoxy(i,y2);
		cputchar('B');
	}

	for(i=y1; i<=y2;i++){
		gotoxy(x1,i);
		cputchar('B');
		gotoxy(x2,i);
		cputchar('B');
	}

	
	for(i=(x1+1);i<x2;i++){
		for(j=(y1+1);j<y2;j++){
			gotoxy(i,j);
			cputchar('R');
		}
	}
	
}

void pixel(int x, int y, unsigned char C){
	union REGS inregs, outregs;
	inregs.x.cx = x;
	inregs.x.dx = y;
	inregs.h.al = C;
	inregs.h.ah = 0x0C;
	int86 (0x10, &inregs, &outregs);
}

void dibujo(){

//DIBUJO DE UNA CASA

	int i;
	int j = 0;
	int k;
	int l = 50;
	setvideomode(0x04);

	//TECHO
	for(i = 50; i > 0; i--){
		pixel(j, i, 7);
		j++;
	}

	while( j < 100){
		pixel(j,i,7);
		j++;
		i++;
	}

	for( k = 0; k < 100; k++){
		pixel(k,50,7);
	}

	//CUADRADO DE LA CASA
	for(l = 50; l < 125; l++){
		pixel(0, l, 2);
		pixel(100, l, 2);
	}

	for(k = 0; k < 100; k++){
		pixel(k, 125, 2);
	}


	//PUERTA DE LA CASA
	for(k = 125; k > 100; k--){
		pixel(42,k,2);
		pixel(52, k, 2);
	}

	for(k = 42; k < 53; k++){
		pixel(k, 100, 2);
	}
}


int main(){
    
	/*
    gotoxy(3, 5);
    mi_pausa();
    */

   //setvideomode(0x04);  

    /*
    unsigned char video = getvideomode();
    printf("El modo de video es: %i", video);
    mi_pausa();
    */

	//clsrc();

	/*
	char prueba;
	textcolor(6);
	textbackground(2);
	
	scanf("%c", &prueba);
	cputchar(prueba);	
	*/


	//dibujarRecuadro(1,1,5,5,1,2);

	dibujo();
	mi_pausa();

	return;
}