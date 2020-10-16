# CS205 C/C++ Program Design - Assignment 3

## Analysis

### Question 1
>  Please implement a function which can compute the dot product of two
vectors. The type of vector elements is float (not double). The function must be robust and cannot crash when you input something incorrectly.

If we use `float *v1 = new float[n]` to create vector with n elements, then the function, which can compute the dot product of two vectors, is easy to implement. However, the other requirement wrote that the function must be robust and cannot crash when we input something incorrectly. It's quite simple but there are many situations to consider, it is very likely that it has not been considered thoroughly. Therefore, I choose to make a general vector class template instead of CLI. According to this idea, we can create random vectors of any length and any type through the following interface:
```cpp
auto random = [] () -> float { return (float)rand()/RAND_MAX; };
auto vector = Vector<int, float>(99).map(random);
```
Next, I must overwrite destructor, copy constructor, copy assignment operator since I am using float pointers. To simplify, we can use `std::vector` to rewrite the core logic in the future. For the sake of intuition, I overwrite the operator *, so we can use vector dot product more intuitively.
```cpp
auto vector_1 = Vector<int, float>(99).map(random);
auto vector_2 = Vector<int, float>(99).map(random);
float result = vector_1 * vector_2;
```
If the type or the syntax is wrong, the compiler will stop, so I only add the process of checking whether the length of two vectors matches before dot product. In addition, in order to avoid bugs, the length and elements of the vector are set as private variables. If we want to process it, we need to go through special getter or setter.

### Question 2
>  Please measure how many milliseconds (or seconds) for vectors which have
more than 200M elements.

According to the [example](https://en.cppreference.com/w/cpp/chrono/time_point), I simply organize the timer utility suitable for this assignment.
```cpp
class Timer {
    public:
        void tic(void);
        void toc(void);
        void print(void);
        int microseconds(void);
        int milliseconds(void);
        int seconds(void);
};
```
In addition, I also define a simple macro to avoid redundant statements:
```cpp
#define TIMEIT(statement) { \
    Timer *_timer = new Timer(); \
    _timer->tic(); \
    statement; \
    _timer->toc(); \
    _timer->print(); \
    delete _timer; \
}

TIMEIT(
    std::cout << vector_1 * vector_2 << std::endl;
);
```

### Question 3
> Improve the efficiency of your source code. Can it be 10 times faster than your first version?

"As you probably know by now, to get the maximum performance benefit from a processor with Hyper-Threading Technology, an application needs to be executed in parallel. Parallel execution requires threads, and threading an application is not trivial. What you may not know is that tools like OpenMP can make the process a lot easier." Therefore, we can use OpenMP to improve the efficiency:
```cpp
template <class I, class T>
class Vector {
    public:
        T dot_mp(Vector<I, T> &other) {
            this->has_same_length_with(other);
            T sum = 0;
            #pragma omp parallel for reduction(+:sum)
            for (I ith=0; ith<this->length; ith++)
                sum += this->data[ith] * other[ith];
            return sum;
        }
};
```
Besides, we can use `g++ -O3` to improve efficiency. Since the question is quite basic, it cannot be 10 times faster than my first version after improving the efficiency, or there are other clever ways I did not think of.

### Question 4
> Compare your implementation of dot product with [OpenBLAS](https://github.com/xianyi/OpenBLAS).

"OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version." The installation and the usage of OpenBLAS can refer to the [wiki](https://github.com/xianyi/OpenBLAS/wiki).


## Code
|filename|description|
|---|---|
|[main.cpp](main.cpp)|Main function, which is the designated start of the program.|
|[vector.h](vector.h)|Vector class template, which contains the main logic of the vector, such as initialization, dot product, etc.|
|[timer.h](timer.h)|Timer utility to measure the number of microseconds (or milliseconds) for certain statements.|
|[Makefile](Makefile)|Configuration file for make utility, which defines set of tasks to be executed.|


## Result & Verification
- Raw loop: 499640.188, 2871µs
```cpp
float sum = 0;
float *pointer_1 = vector_1.get_data();
float *pointer_2 = vector_2.get_data();
for (int ith=0; ith<2000000; ith++)
    sum += pointer_1[ith] * pointer_2[ith];
cout << sum << endl;
```

- Class template for loop: 499640.188, 7631µs
```cpp
cout << vector_1 * vector_2 << endl;
```

- Class template for loop with OpenMP: 499910.656, 2563µs
```cpp
cout << vector_1.dot_mp(vector_2) << endl;
```

- OpenBLAS: 499912.5, 753µs
```cpp
cout << cblas_sdot(2000000, vector_1.get_data(), 1, vector_2.get_data(), 1) << endl;
```

According to the data, the error of dot product between vectors with 200M 0-1 random elements is within 300.


## Difficulties & Solutions
|Difficulties|Solutions|
|---|---|
|Class template and other concepts|https://en.cppreference.com/|
|Error message I haven't seen|https://stackoverflow.com/ and https://stackexchange.com/ and https://github.com/ |
|Installation and usage of OpenBLAS|Github wiki and official documentation|


## References
- https://stackoverflow.com/questions/63413418/free-double-free-detected-in-tcache-2
- https://en.cppreference.com/w/cpp/chrono/time_point
- https://stackoverflow.com/questions/12386467/g-compile-options-g-debug-and-o-optimization
- https://cmake.org/cmake/help/latest/guide/tutorial/index.html
- https://github.com/xianyi/OpenBLAS
- https://software.intel.com/content/www/us/en/develop/articles/getting-started-with-openmp.html
