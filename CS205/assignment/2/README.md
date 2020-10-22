# CS205 C/C++ Program Design - Assignment 2

## Analysis
### Basic requirements
> Question 5. It can support arbitrary precision.

All variables and functions are stored in the `map`, which means that the keys type or the values type of a particular map should be consistent, so I chose `double` like MATLAB. At the same time, for scalability, I use template to construct `Globals`: `template<class REAL = double, class INTEGER = int> class GLobals { ... };`. Although I can extend class `BigInteger` in [Assignment 1](../1/biginteger.h) to any real numbers and use it to construct `GLobals<BigRealNumber, BigInteger> globals`, all math functions(`sin`, `cos`, etc.) have `double` or `long double` as their return value type and parameter type, which means if I want to use mathematical functions, I need to extend the domain and range from `double` to any real number. Obviously simply using `double` for type conversion will cause unpredictable problems, therefore, I just provide the possibility of large number operations (i.e. class template), but in the end, `double` is used as all variable types.

> Question 1. When you run your program and input an express in a line, it can output the correct results. The operator precedence (order of operations) should be correct.

> Question 3. Variables can be defined as follows.

> Question 4. Some math functions can be supported.

Also for versatility, I treat binary operation(+, -, \*, /, etc.) as binary function, and recursion is used when judging the parameters of the function, so I divide the function into void function(`function<REAL()>`, i.e. function without parameters), unary function(`function<REAL(REAL)>`), binary function(`function<REAL(REAL, REAL)>`) and variable function(`function<REAL(string, REAL)>`, for example, convert `x+=3` to `+=("x", 3)`). Therefore, parameter assignment and mathematical function call can all be reduced to the same question.

We can see which functions can be called in the compilation result:
```shell
$ ./math

>>> functions
...

 Void functions:
    rand, time,

Unary functions:
    !, +, -, abs, acos, acosh, asin, asinh, atan, atanh, ceil, cos, cosh, erf, exp, floor, ln, log10, log2, print, round, sin, sinh, sqrt, tan, tanh,

Binary functions:
    !=, %, &, &&, *, +, -, /, <, <=, ==, >, >=, ^, |, ||,

Variable functions:
    %=, &=, *=, +=, -=, /=, <<=, =, >>=, ^=, |=,
```

The definition of some functions is basically the same, thanks to the macro, we can omit a lot of duplicate content:
```C++
...

#define ZF(o, s) this->void_functions[#o] = [] () -> REAL { s; };
#define UF(o, s) this->unary_functions[#o] = [] (REAL number) -> REAL { s; };
#define UFD(o) UF(o, return o(number);)
#define BFD(o) BF(o, return left o right;)
#define BF(o, s) this->binary_functions[#o] = [] (REAL left, REAL right) -> REAL { s; };
#define VF(o, s) this->variable_functions[#o] = [this] (string key, REAL value) -> REAL { s; return this->variables[key]; };
#define VFD(o) VF(o, this->variables[key] o value;)

...

template<class REAL = double, class INTEGER = int>
class Globals {
    public:
        map<string, function<REAL()>> void_functions;
        map<string, function<REAL(REAL)>> unary_functions;
        map<string, function<REAL(REAL, REAL)>> binary_functions;
        map<string, function<REAL(string, REAL)>> variable_functions;
        map<string, REAL> variables;

        Globals() {
            // void, unary and binary functions
            UFD(+);UFD(-);UFD(!);UFD(cos);UFD(sin); ...
            BFD(+);BFD(-);BFD(*);BFD(/);BFD(>);BFD(<); ...

            ZF(rand, return (double)rand()/RAND_MAX;);
            ZF(time, return time(0);)

            UF(ln, return log(number););
            UF(print, cout << number << endl; return number;);

            BF(%, return fmod(left, right););
            BF(^, return pow(left, right););
            ...

            // functions involving variables
            VFD(=);VFD(+=);VFD(-=);VFD(*=);VFD(/=);

            VF(%=, this->variables[key] = fmod(this->variables[key], value););
            VF(^=, this->variables[key] = pow(this->variables[key], value););
            ...
        }
};
```

After solving the problem of function calls, then we need to analyze how to perform different functions according to the input text. Because the results are real-time, we need an [interpreter](https://en.wikipedia.org/wiki/Interpreter_(computing)). After going through the explanation briefly, without the support of the compilation principle, we do not consider optimization and other issues involving knowledge blind spots. So from the input text to the result of the calculation, we need to do the following three steps(approximately):
1. Preprocessing: remove comments, split and merge lines, etc;
2. Tokenization: turn source code into tokens;
3. Parse: generate immediate instructions.

According to the previous analysis, we define the following tokens(also need to store the corresponding data):
```C++
struct token {
    enum TokenType {
        VOID_FUNCTION, UNARY_FUNCTION, BINARY_FUNCTION, VARIABLE_FUNCTION, NUMBER,
        VARIABLE, LEFT_PARENTHESE, RIGHT_PARENTHESE, LEFT_BRACE, RIGHT_BRACE, EMPTY
    } type;
    string value;
};
```

Next we construct the interpreter(due to "historical" problems, the actual code is slightly different from this architecture):
```C++
template<class REAL = double, class INTEGER = int>
class Interoreter {
    public:
        run(string code);

    private:
        Globals<REAL, INTEGER> globals;

        string preprocess(string code);
        list<string> split_lines(string code);
        list<token> split_tokens(string line);
        REAL parse(list<token> tokens);
};
```

Because of the lack of knowledge about the compilation principle, the logic part of the code will not be expanded, although it can run successfully, there is a suspected deviation from the standard flow.

> Question 2. Use parentheses to enforce the priorities.

Since brackets are not used elsewhere just to implement the calculator, to make the discussion less difficult, we use brackets to force priority. Moreover, the binary operators are treated as binary functions, which are stored in `map<string, function<REAL(REAL, REAL)>>`, if the priority between each symbol is clear, you need to introduce variables to store the priority, and except for the addition, subtraction, multiplication and division, the use of each priority range is small, at the same time a small number of priorities will cause the code inelegant, so the final solution is to use brackets to force the priority, tokens are parsed in order from left to right(i.e. the content in the brackets is parsed first in the parsing process).

### Extra features
1. Use `...` to continue the content on the next line, use `;` to end the current line
2. Use `_` to automatically store the result of the previous statement
3. command system:
    - exit: terminate program
    - variables: show all variables
    - functions: show all functions
    - commands|help: show all commands
    - time [on|off]: whether to record the running time
    - display [on|off]: whether to display result automatically

### Demo
The following content is from [demo.math](demo.math), which basically shows all the features.
```
# comment, the result shall be 13.068672553556999
time on
display off

xx = { ...
    {1 + 2} * {-3.14e-2 + sqrt(pi)} / {sin(cos(1+pi)) + e} ...
}
ln(pi)
yy = {xx + _} ; yy *= {e+1}

print(yy)
```


## Code
|filename|description|
|---|---|
|[main.cpp](main.cpp)|Main function, which is the designated start of the program.|
|[models.h](models.h)|Interpreter class template, which contains the main logic of the interpreter, such as tokenize, parse, etc.|
|[timer.h](timer.h)|Timer utility to measure the number of microseconds (or milliseconds) for certain statements.|
|[utils.h](utils.h)|Utility to process IO.|
|[Makefile](Makefile)|Configuration file for make utility, which defines set of tasks to be executed.|
|[demo.math](demo.math)|Demo files for testing program.|
|[demo.cpp](demo.cpp)|C++ file for comparison, which has the same function as [demo.math](demo.math).|
|[demo.py](demo.py)|Python file for comparison, which has the same function as [demo.math](demo.math).|


## Result & Verification
The program runs correctly, that is, the result is consistent with the C++ and Python of the same logic.

- windows:
```shell
$ make compare

=== Math ===
./math demo.math
13.0687
Time has elapsed 475µs ≈ 0ms ≈ 0s.

=== C++ ===
g++ demo.cpp -o _ && ./_ demo.math
13.0687
Time has elapsed 375µs ≈ 0ms ≈ 0s.

=== Python ===
python demo.py
13.068672553556999
Time has elapsed 366.60µs ≈ 0.37ms ≈ 0.00s.
```

- linux:
```shell
$ make compare

=== Math ===
./math demo.math
13.0687
Time has elapsed 231µs ≈ 0ms ≈ 0s.

=== C++ ===
g++ demo.cpp -o _ && ./_ demo.math
13.0687
Time has elapsed 33µs ≈ 0ms ≈ 0s.

=== Python ===
python demo.py
13.068672553556999
Time has elapsed 273.10µs ≈ 0.27ms ≈ 0.00s.
```


## Difficulties & Solutions
|Difficulties|Solutions|
|---|---|
|Tokenize, parse and other concepts|https://en.wikipedia.org/wiki/ and https://github.com/|
|Error message I haven't seen|https://stackoverflow.com/ and https://stackexchange.com/ and https://github.com/ |
|Storage format of variables and functions|https://docs.python.org/3/library/functions.html#globals|


## References
- http://www.cplusplus.com/reference/string/string/
- http://www.cplusplus.com/reference/vector/vector/
- http://www.cplusplus.com/reference/map/map/
- http://www.cplusplus.com/reference/regex/
- http://www.cplusplus.com/reference/list/list/
- https://en.cppreference.com/w/cpp/chrono/time_point
- https://en.cppreference.com/w/cpp/language/enum
- https://en.cppreference.com/w/cpp/language/lambda
- https://zhuanlan.zhihu.com/p/143884880
- https://en.wikipedia.org/wiki/Interpreter_(computing)
- https://stackoverflow.com/questions/110157/how-to-retrieve-all-keys-or-values-from-a-stdmap-and-put-them-into-a-vector
- https://stackoverflow.com/questions/2866380/how-can-i-time-a-code-segment-for-testing-performance-with-pythons-timeit
