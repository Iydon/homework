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

    // Globals<double, int> globals;

    // cout << globals.unary_functions["ln"](globals.variables["e"]) << endl;
    // cout << globals.variable_functions["+="]("_", 2) << endl;
    // cout << globals.variable_functions["<<="]("_", 1) << endl;
    // cout << globals.unary_functions["print"](globals.variables["_"]) << endl;
    // cout << globals.binary_functions["-"](globals.variables["pi"], 3) << endl;

    // cout << globals.variable_functions["="]("x", 1) << endl;
    // cout << globals.variables["x"] << endl;

    // Read read;
    // cout << read.from_console() << endl;
    // cout << read.from_file(__FILE__) << endl;
}
