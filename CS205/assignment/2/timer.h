#pragma once


#include <chrono>
#include <ctime>
#include <iostream>


#define TIMEIT(statement) { \
    Timer *_timer = new Timer(); \
    _timer->tic(); \
    statement; \
    _timer->toc(); \
    _timer->print(); \
    delete _timer; \
}


using namespace std;


class Timer {
    public:
        chrono::time_point<chrono::steady_clock> start;
        chrono::time_point<chrono::steady_clock> end;

        void tic(void) {
            this->start = chrono::steady_clock::now();
        }

        void toc(void) {
            this->end = chrono::steady_clock::now();
        }

        void print(void) {
            cout << "Time has elapsed "
                << this->microseconds() << "µs ≈ "
                << this->milliseconds() << "ms ≈ "
                << this->seconds() << "s." << endl;
        }

        int microseconds(void) {
            return chrono::duration_cast<chrono::microseconds>(
                this->end - this->start
            ).count();
        }

        int milliseconds(void) {
            return chrono::duration_cast<chrono::milliseconds>(
                this->end - this->start
            ).count();
        }

        int seconds(void) {
            return chrono::duration_cast<chrono::seconds>(
                this->end - this->start
            ).count();
        }
};


class Timer2 {
    public:
        time_t  start;
        time_t  end;

        void tic(void) {
            this->start = time(0);
        }

        void toc(void) {
            this->end = time(0);
        }

        void print(void) {
            cout << "Time has elapsed "
                << this->microseconds() << "µs ≈ "
                << this->milliseconds() << "ms ≈ "
                << this->seconds() << "s." << endl;
        }

        int microseconds(void) {
            return 1e6 * this->seconds();
        }

        int milliseconds(void) {
            return 1e3 * this->seconds();
        }

        int seconds(void) {
            return (double)(this->end - this->start);
        }
};
