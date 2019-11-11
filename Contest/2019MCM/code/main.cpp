/*
 * @Time     : 2019/01/25 13:00
 * @Author   : Iydon
 * @File     : main.cpp
 */

#include <stdio.h>
#include "time.h"
#include "environ.h"
#include "dragon.h"
#include "interface.h"
#include "utils/plot.h"
using namespace std;

int main() {
    int YEAR = 1000;
    int DAY  = 365;
    int MIN  = 60 * 24;
    double DELTA = 1.0 / DAY / MIN;
    Time time = Time(0, 0, 0);
    int y, d, m;

    Dragon Smaug = Dragon(1);
    Smaug.set_attributions(0, true, 10.0, 10.0, 1.0, 0.0, 0.0, 1.0);

    Environ dessert = Environ(0);
    dessert.set_attributions(27.0, 0.7, 1000.0);

    double xx[YEAR*DAY];
    double yy[YEAR*DAY];

    for (y=0; y<YEAR; y++) {
        for (d=0; d<DAY; d++) {
            for (m=0; m<MIN; m++) {
                time.set_minute(m);
                Smaug.simulate(DELTA, time, dessert);
                dessert.simulate(time);
            }
            xx[y*DAY+d] = Smaug.get_x();
            yy[y*DAY+d] = Smaug.get_y();
            time.set_day(d);
        }
        time.set_year(y);
    }

    plot(xx, yy, YEAR*DAY, "result.png");

    Smaug.print_info();
}
