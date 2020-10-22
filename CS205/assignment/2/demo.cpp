#include <iostream>
#include <cmath>

#include "timer.h"


#define PI 3.14159265358979323846
#define E 2.71828182845904523536


using namespace std;


int main() {
    TIMEIT(
        double xx = xx = (1+2) * (-3.14e-2+sqrt(PI)) / (sin(cos(1+PI))+E);
        double _ = log(PI);
        double yy = xx + _;
        yy *= E + 1;
        cout << yy << endl;
    );
}
