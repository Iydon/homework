/*
 * author: Iydon Liang
 * time: 2019/10/01 21:35:00
 * compile: `g++ -fconcepts 4.cpp -o 4.out`
 */
#include <cstdio>
#include <math.h>
#include <time.h>

#define _rand_ (double)rand()/RAND_MAX
#define _self_ [](double x)->double{return x;}
#define _len_(x) (sizeof(x)/sizeof(x[0]))
#define _abs_(x) (x>0 ? x:-x)
#define _tic_ int tic = time(0)
#define _toc_ int toc = time(0)
#define _debug_ true


double randn(double mu=0., double sigma=1.) {
    double V1, V2, S;
    do {
        V1 = 2*_rand_ - 1;
        V2 = 2*_rand_ - 1;
        S = V1*V1 + V2*V2;
    } while(S>=1 || S==0);
    double _randn = V1 * sqrt(-2*log(S)/S);

    return sigma*_randn + mu;
}

double E(double array[], int length, auto key) {
    double result = 0.;
    for (int ith=0; ith<length; ith++) {
        result += key(array[ith]);
    }
    return result / length;
}

double S2(double array[], int length, bool unbiased=true) {
    double mean = E(array, length, _self_);
    double result = 0.;
    double delta;
    for (int ith=0; ith<length; ith++) {
        delta = array[ith] - mean;
        result += delta * delta;
    }
    if (unbiased) return result / (length-1);
    else return result / length;
}

// main function
int main() {
    // set the random seed
    srand((int)time(0));
    double mu = 0.;
    double sigma  = 1.;
    double sigma2 = sigma * sigma;

    // new sample array
    int sample_length = 1024;
    double sample[sample_length];
    double unbiased, biased;

    // new experiment array
    int experiment_length = 65536;
    int experiment[2] = {0, 0}; // {unbiased, biased}
    int record[2] = {0, 0}; // {exceed, behind}

    // experiment
    _tic_;
    for (int ith=0; ith<experiment_length; ith++) {
        // initialize sample
        for (int jth=0; jth<sample_length; jth++)
            sample[jth] = randn(mu, sigma);

        // calculate S^2
        unbiased = S2(sample, sample_length, true);
        biased   = S2(sample, sample_length, false);

        if (_abs_(unbiased-sigma2) < _abs_(biased-sigma2))
            experiment[0] += 1;
        else experiment[1] += 1;
        if (experiment[0] > experiment[1])
            record[0] += 1;
        else if (experiment[0] < experiment[1])
            record[1] += 1;
    }
    _toc_;

    // print result
    printf("unbiased: %d\n", experiment[0]);
    printf("bias:     %d\n", experiment[1]);
    printf("exceed:   %d\n", record[0]);
    printf("behind:   %d\n", record[1]);
    printf("elapsed time(s): %d\n", toc-tic);
}
