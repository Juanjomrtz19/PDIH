#include <stdio.h>
#include <dos.h>
#include <stdlib.h>

main () {
	FILE *log;
	struct date d;
	struct time t;

	if ((log = fopen("\\DOS\\INDICE\\SESIONES.LOG","at"))==NULL) return 1;

	getdate(&d);
	gettime(&t);
	fprintf (log,"%02d/%02d/%02d  %02d:%02d:%02d  %s\n",
				d.da_day,d.da_mon,d.da_year,t.ti_hour,t.ti_min,t.ti_sec,
				getenv("CONFIG"));
	fclose(log);

	return 0;
}
