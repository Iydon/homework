#include <iostream>

#include "models.h"
#include "utils.h"


using namespace std;


int main(int argc, char *argv[]) {
    Interpreter interpreter;
    string code;

    switch (argc) {
        case 1:
            while (true) {
                code = read::from_console();
                interpreter.run(code);
            }
            break;

        case 2:
            if (!(strcmp(argv[1], "-h")&&strcmp(argv[1], "--help"))) {
                cout << "用法：math [文件]..." << endl;
                break;
            }

        default:
            for (int ith=1; ith<argc; ith++) {
                cout << argv[ith] << ":" << endl;
                interpreter.run(read::from_file(argv[ith]));
            }
    }
}
