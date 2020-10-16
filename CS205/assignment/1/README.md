# CS205 C/C++ Program Design - Assignment 1

## Analysis
    Things to consider for a big int class:
    1. Mathematical operators: +, -, /, *, % Don't forget that your class may be on either side of the operator, that the operators can be chained, that one of the operands could be an int, float, double, etc.
    2. I/O operators: >>, << This is where you figure out how to properly create your class from user input, and how to format it for output as well.
    3. Conversions/Casts: Figure out what types/classes your big int class should be convertible to, and how to properly handle the conversion. A quick list would include double and float, and may include int (with proper bounds checking) and complex (assuming it can handle the range).

Therefore, we can organize the following basic structure:

```cpp
class BigInteger {
    public:
        // Constructors
        Bigint();
        Bigint(long long);
        Bigint(std::string);
        Bigint(const Bigint&);

        // Adding
        Bigint operator+(Bigint const &) const;
        Bigint &operator+=(Bigint const &);
        Bigint operator+(long long const &) const;
        Bigint &operator+=(long long);

        // Subtraction
        Bigint operator-(Bigint const &) const;
        Bigint &operator-=(Bigint const &);

        // Multiplication
        Bigint operator*(Bigint const &);
        Bigint &operator*=(Bigint const &);
        Bigint operator*(long long const &);
        Bigint &operator*=(int const &);

        // Compare
        bool operator<(const Bigint &) const;
        bool operator>(const Bigint &) const;
        bool operator<=(const Bigint &) const;
        bool operator>=(const Bigint &) const;
        bool operator==(const Bigint &) const;
        bool operator!=(const Bigint &) const;

        // Allocation
        Bigint operator=(const long long &);

        // Access
        int operator[](int const &);

        // Input & Output
        friend std::istream &operator>>(std::istream &, Bigint &);
        friend std::ostream &operator<<(std::ostream &, Bigint const &);

    private:
        std::vector<int> numbers;
        bool positive;
        int compare(Bigint const &) const; // 0: a==b, -1: a<b, 1: a>b
};
```


## Code
|filename|description|
|---|---|
|[main.cpp](main.cpp)|Main function, which is the designated start of the program.|
|[biginteger.h](biginteger.h)|Big integer class, which contains the main logic of the big integer, such as addition, subtraction, multiplication and division.|
|[Makefile](Makefile)|Configuration file for make utility, which defines set of tasks to be executed.|


## Result & Verification
- Example 1
```
Please input two integers, next I will multiply the two numbers.
-2 3

-6
```

- Example 2
```
Please input two integers, next I will multiply the two numbers.
31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
27182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274

853973422267356706546355086954657449503488853576511496187960113017922861115733080757256386971047394360418507658574182427535480134567986011372683865883504670910306252214972528542462869537848950160622046
```

- Example 3
```
Please input two integers, next I will multiply the two numbers.
a 3

The integers you input are not all valid.
```

- Example 4
```
Please input two integers, next I will multiply the two numbers.
-2 03

The integers you input are not all valid.
```


## Difficulties & Solutions
|Difficulties|Solutions|
|---|---|
|Large number operations|Refer to https://github.com/kasparsklavins/bigint|
|Use regex to check whether the number is valid|https://en.cppreference.com/w/cpp/header/regex|
|Error message I haven't seen|https://stackoverflow.com/ and https://stackexchange.com/ and https://github.com/ |


## References
- https://stackoverflow.com/questions/269268/how-to-implement-big-int-in-c
- https://github.com/kasparsklavins/bigint
- https://google.github.io/styleguide/cppguide.html
