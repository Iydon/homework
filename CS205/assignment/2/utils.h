#pragma once


#include <fstream>
#include <iostream>


using namespace std;


class read {
    /*
     * 读取代码
     */
    public:
        static string from_console() {
            /*
             * 空行结束
             */
            string line, result = "";
            cout << ">>> " << ends;
            while (true) {
                getline(cin, line);
                if (line.empty())
                    break;
                result += line + "\n";
                cout << "... " << ends;
            }
            return result;
        }

        static string from_file(string filename) {
            /*
             * EOF 结束
             */
            ifstream f(filename);
            string line, result = "";
            while (getline(f, line))
                result += line + "\n";
            return result;
        }
};
