#include "timer.cpp"
#include "vector.cpp"

#define number 2000000
#define integer int
#define real float


int main() {
    srand((int)(time(NULL)));
    auto random = [] () -> real { return (real)rand()/RAND_MAX; };
    auto v1 = Vector<integer, real>(number).map(random);
    auto v2 = Vector<integer, real>(number).map(random);
    Timer timer;

    timer.tic();
    v1 * v2;
    timer.toc();
    timer.print();
}
