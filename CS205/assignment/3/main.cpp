#include <iostream>
#include <iomanip>

#include "timer.h"
#include "vector.h"

#include "cblas.h"


#define NUMBER 2000000
#define INTEGER int
#define REAL float


using namespace std;


int main() {
    // 配置及变量初始化
    srand((int)(time(0)));
    cout << setprecision(9);
    auto random = [] () -> REAL { return (REAL)rand()/RAND_MAX; };
    auto vector_1 = Vector<INTEGER, REAL>(NUMBER).map(random);
    auto vector_2 = Vector<INTEGER, REAL>(NUMBER).map(random);

    // 1. Raw
    TIMEIT(
        REAL sum = 0;
        REAL *pointer_1 = vector_1.get_data();
        REAL *pointer_2 = vector_2.get_data();
        for (INTEGER ith=0; ith<NUMBER; ith++)
            sum += pointer_1[ith] * pointer_2[ith];
        cout << sum << endl;
    );

    // 2. For loop
    TIMEIT(
        cout << vector_1.dot(vector_2) << endl;
    );

    // 3. For loop with OpenMP
    TIMEIT(
        cout << vector_1.dot_mp(vector_2) << endl;
    );

    // 4. OpenBLAS
    TIMEIT(
        cout << cblas_sdot(NUMBER, vector_1.get_data(), 1, vector_2.get_data(), 1) << endl;
    );
}
