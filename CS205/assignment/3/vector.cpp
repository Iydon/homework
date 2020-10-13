#include <iostream>


template <class I, class T>
class Vector {
    public:
        // 构造函数与析构函数
        Vector(I length) {
            this->length = length;
            this->data = new T[length];
        }

        Vector(Vector &other) {
            this->initialize(other.length, other.data);
        }

        ~Vector(void) {
            delete [] this->data;
        }

        // 运算符重载
        T &operator[](I index) {
            return this->data[
                (index%this->length+this->length)%this->length
            ];
        }

        Vector<I, T> &operator=(Vector<I, T> &other) {
            if (this != &other) {
                this->initialize(other.length, other.data);
            }
            return *this;
        }

        T operator*(Vector<I, T> &other) {
            return this->dot(other);
        }

        Vector<I, T> operator+(Vector<I, T> &other) {
            return this->plus(other);
        }

        Vector<I, T> operator-(Vector<I, T> &other) {
            return this->minus(other);
        }

        // 功能性函数
        I number(void) {
            return this->length;
        }

        Vector<I, T> &map(auto function) {
            for (I ith=0; ith<this->length; ith++) {
                this->data[ith] = function();
            }
            return *this;
        }

        void unify(T value) {
            this->map([value] () -> T { return value; });
        }

        void print(void) {
            std::cout << "<Vector(" << this->length << ") @ (";
            for (I ith=0; ith<this->length; ith++) {
                std::cout << this->data[ith] << ", ";
            }
            std::cout << ")>" << std::endl;
        }

        // 二元运算符
        T dot(Vector<I, T> &other) {
            this->has_same_length_with(other);
            T sum = 0;
            for (I ith=0; ith<this->length; ith++) {
                sum += this->data[ith] * other[ith];
            }
            return sum;
        }

        Vector<I, T> plus(Vector<I, T> &other) {
            this->has_same_length_with(other);
            Vector<I, T> result(this->length);
            for (I ith=0; ith<this->length; ith++) {
                result[ith] = this->data[ith] + other[ith];
            }
            return result;
        }

        Vector<I, T> minus(Vector<I, T> &other) {
            this->has_same_length_with(other);
            Vector<I, T> result(this->length);
            for (I ith=0; ith<this->length; ith++) {
                result[ith] = this->data[ith] - other[ith];
            }
            return result;
        }

    private:
        // 私有变量（不允许外部修改）
        I length;
        T *data = NULL;

        // 私有函数（仅用作合并重复项）
        void has_same_length_with(Vector<I, T> &other) {
            if (this->length != other.length) {
                throw "Length does not match.";
            }
        }

        void initialize(I length, T *data) {
            delete [] this->data;
            this->length = length;
            this->data = new T[length];
            for (I ith=0; ith<length; ith++) {
                this->data[ith] = data[ith];
            }
        }
};
