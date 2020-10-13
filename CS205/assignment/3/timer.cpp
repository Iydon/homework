#include <chrono>
#include <ctime>
#include <iostream>

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
