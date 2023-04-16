#include <ncurses.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define DELAY 100000

// Dimensiones del campo de juego
const int ANCHO = 60;
const int ALTO = 30;


// Coordenadas iniciales de la pelota y las paletas
int pelotax = ANCHO / 2;
int pelotay = ALTO / 2;
int jugador1x = 1;
int jugador1y = ALTO / 2 - 2;
int jugador2x = ANCHO - 2;
int jugador2y = ALTO / 2 - 2;
int puntos1 = 0;
int puntos2 = 0;
int rows, cols;
bool continuar = true;
bool seguir = true;
// Velocidad de la pelota
int movpelotax = -1;
int movpelotay = -1;

// Función para dibujar el campo de juego
void campo(){
    // Limpia la pantalla
    clear();
    // Dibuja los bordes
    for (int i = 0; i < ANCHO; i++){
        mvprintw(0, i, "-");
        mvprintw(ALTO - 1, i, "-");
    }
    for (int i = 1; i < ALTO - 1; i++){
        mvprintw(i, 0, "|");
        mvprintw(i, ANCHO - 1, "|");
    }
    // Dibuja la pelota y las paletas
    mvprintw(pelotay, pelotax, "O");
    for (int i = 0; i < 4; i++){
        mvprintw(jugador1y + i, jugador1x, "|");
        mvprintw(jugador2y + i, jugador2x, "|");
    }

    mvprintw(ALTO + 5, 1, "%d", puntos1);
    mvprintw(ALTO + 5, ANCHO -1, "%d", puntos2);

    // Refresca la pantalla
    refresh();
}

int main(){
    
    initscr();

    //NUEVA VENTANA
    if (has_colors() == FALSE) {
        endwin();
        printf("El terminal no tiene soporte de color \n");
        exit(1);
    }
    start_color();
    init_pair(1, COLOR_YELLOW, COLOR_GREEN);
    init_pair(2, COLOR_BLACK, COLOR_WHITE);
    init_pair(3, COLOR_WHITE,COLOR_BLUE);
    clear();
    refresh();
    getmaxyx(stdscr, rows, cols);

    noecho();
    curs_set(0);
    WINDOW * instrucciones = newwin(rows, cols, 0, 0);
    wbkgd(instrucciones, COLOR_PAIR(2));
    mvwprintw(instrucciones, 1, 1, "Realizado por Juan José Martínez Águila, github JuanjoGG69");
    mvwprintw(instrucciones, 2, 1, "Controles jugador izquierda, arriba w y abajo s");
    mvwprintw(instrucciones, 3, 1, "Controles jugador derecha, arriba p y abajo l");
    mvwprintw(instrucciones, 4, 1, "El juego acaba cuando algun jugador pulse la tecla e o quien llegue a tres puntos antes");
    wrefresh(instrucciones);
    getch();

    timeout(0);

    campo();

    while(seguir){
        int tecla = getch();
        switch(tecla){
            case 'e':
                endwin();
                return 0;
            case 'w':
                if(jugador1y > 1){
                    jugador1y--;
                }
                break;
            case 's':
                if(jugador1y + 4 < ALTO - 1 ){
                    jugador1y++;
                }
                break;
            case 'p':
                if(jugador2y >1){
                    jugador2y--;
                }
                break;
            case 'l':
                if(jugador2y + 4 < ALTO - 1){
                    jugador2y++;
                }
                break;
        }

        pelotax += movpelotax;
        pelotay += movpelotay;

        if(pelotay <= 0 || pelotay >= ALTO - 1){
            movpelotay = -movpelotay;
        }

        if(pelotax <= 0 || pelotax >= ANCHO - 1){
            
            if(pelotax >= ANCHO -1){
                puntos1++;
            }
            if(pelotax <= 0){
                puntos2++;
            }
            pelotax = ANCHO / 2;
            pelotay = ALTO / 2;
        }

        if (pelotax == jugador1x + 1 && (pelotay >= jugador1y && pelotay < jugador1y + 4)){
            movpelotax = -movpelotax;
        }

        if (pelotax == jugador2x - 1 && (pelotay >= jugador2y && pelotay < jugador2y + 4)){
            movpelotax = -movpelotax;
        }

        campo();
        usleep(DELAY);
        if(puntos1 == 3 || puntos2 == 3){
            timeout(-1);
            WINDOW * final = newwin(rows, cols, 0, 0);
            wbkgd(final, COLOR_PAIR(3));
            mvwprintw(final, 1, 1, "___________________________________GAME OVER_________________________________");
            mvwprintw(final, 2, 1, "Jugador derecha:" );
            mvwprintw(final, 2, 20,"%d",puntos1);
            mvwprintw(final, 3, 1, "Jugador izquierda:");
            mvwprintw(final, 3, 20, "%d", puntos2);
            mvwprintw(final,4 , 0,"Si desea iniciar una partida pulse la tecla c, si desea salir pulse cualquier otra tecla");
            wrefresh(final);
            char tecla = getch();
            if(tecla != 'c'){
                seguir = false;
            }
            else{
                timeout(0);
                puntos1 = 0;
                puntos2 = 0;
            }
        }
    }

    endwin();
    return 0;
}
