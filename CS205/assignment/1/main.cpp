#include <iostream>
#include <regex>

#include "biginteger.h"


using namespace std;


int main() {
    regex  pattern("-?([1-9][0-9]*|0)");
    string expression_1, expression_2;
    BigInteger number_1, number_2;

    cout << "Please input two integers, next I will multiply the two numbers." << endl;
    cin >> expression_1 >> expression_2;
    if (regex_match(expression_1, pattern) && regex_match(expression_2, pattern)) {
        number_1 = expression_1;
        number_2 = expression_2;
        cout << number_1 * number_2 << endl;
    } else {
        cout << "The integers you input are not all valid." << endl;
    }
}
