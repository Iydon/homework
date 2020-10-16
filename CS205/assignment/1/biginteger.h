// https://github.com/kasparsklavins/bigint
#pragma once


#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>


class BigInteger {
    private:
        std::vector<int> numbers;
        bool positive;
        int base;
        unsigned int skip;
        static const int default_base = 1000000000;

        int segment_length(int segment) const {
            int length = 0;
            while (segment) {
                segment /= 10;
                ++length;
            }
            return length;
        }

        BigInteger pow(int const &power, std::map<int, BigInteger> &lookup) {
            if (power == 1)
                return *this;
            if (lookup.count(power))
                return lookup[power];
            int closest_power = 1;
            while (closest_power < power)
                closest_power <<= 1;
            closest_power >>= 1;
            if (power == closest_power)
                lookup[power] = this->pow(power/2, lookup) * this->pow(power/2, lookup);
            else
                lookup[power] = this->pow(closest_power, lookup) * this->pow(power-closest_power, lookup);
            return lookup[power];
        }

        int compare(BigInteger const &a) const {
            // 0: a==b, -1: a<b, 1: a>b
            if (this->positive && !a.positive)
                return 1;
            if (!this->positive && a.positive)
                return -1;
            int check = 1;
            if (!this->positive && !a.positive)
                check = -1;
            if (this->numbers.size() < a.numbers.size())
                return -1 * check;
            if (this->numbers.size() > a.numbers.size())
                return check;
            for (size_t ith(this->numbers.size()); ith>0; --ith) {
                if (this->numbers[ith-1] < a.numbers[ith-1])
                    return -1 * check;
                if (this->numbers[ith-1] > a.numbers[ith-1])
                    return check;
            }
            return 0;
        }

    public:
        // Constructors
        BigInteger() {
            this->positive = true;
            this->base = this->default_base;
            this->skip = 0;
        }

        BigInteger(long long value) {
            this->base = this->default_base;
            this->skip = 0;
            this->positive = value >= 0;
            if (!this->positive)
                value *= -1;
            while (value) {
                this->numbers.push_back((int) (value % this->base));
                value /= this->base;
            }
        }

        BigInteger(std::string value) {
            int size = value.length(), length, num, prefix, ith;
            this->base = this->default_base;
            this->skip = 0;
            this->positive = value[0] != '-';
            while (true) {
                if (size <= 0)
                    break;
                if (!this->positive && size<=1)
                    break;
                length = 0;
                num = 0;
                prefix = 1;
                for (ith=size-1; ith>=0&&ith>=size-9; --ith) {
                    if (value[ith]<'0' || value[ith]>'9')
                        break;
                    num += (value[ith] - '0') * prefix;
                    prefix *= 10;
                    ++length;
                }
                this->numbers.push_back(num);
                size -= length;
            }
        }

        BigInteger(const BigInteger &b) : numbers(b.numbers), positive(b.positive),
            base(b.base), skip(b.skip) { }

        // Adding
        BigInteger operator+(BigInteger const &b) const {
            BigInteger c = *this;
            c += b;
            return c;
        }

        BigInteger &operator+=(BigInteger const &b) {
            if (!b.positive)
                return *this -= b;
            std::vector<int>::iterator it1 = this->numbers.begin();
            std::vector<int>::const_iterator it2 = b.numbers.begin();
            int sum = 0;
            while (it1!=this->numbers.end() || it2!=b.numbers.end()) {
                if (it1 != this->numbers.end()) {
                    sum += *it1;
                } else {
                    this->numbers.push_back(0);
                    it1 = this->numbers.end() - 1;
                }
                if (it2 != b.numbers.end()) {
                    sum += *it2;
                    ++it2;
                }
                *it1 = sum % this->base;
                ++it1;
                sum /= this->base;
            }
            if (sum)
                this->numbers.push_back(1);
            return *this;
        }

        BigInteger operator+(long long const &b) const {
            BigInteger c = *this;
            c += b;
            return c;
        }

        BigInteger &operator+=(long long b) {
            std::vector<int>::iterator it = this->numbers.begin();
            if (skip > this->numbers.size()) {
                this->numbers.insert(this->numbers.end(),
                    this->skip-this->numbers.size(), 0
                );
            }
            it += skip;
            bool initial_flag = true;
            while (b || initial_flag) {
                initial_flag = false;
                if (it != this->numbers.end()) {
                    *it += b % this->base;
                    b /= this->base;
                    b += *it / this->base;
                    *it %= this->base;
                    ++it;
                } else {
                    this->numbers.push_back(0);
                    it = this->numbers.end() - 1;
                }
            }
            return *this;
        }

        // Subtraction
        BigInteger operator-(BigInteger const &b) const {
            BigInteger c = *this;
            c -= b;
            return c;
        }

        BigInteger &operator-=(BigInteger const &b) {
            std::vector<int>::iterator it1 = this->numbers.begin();
            std::vector<int>::const_iterator it2 = b.numbers.begin();
            int dif = 0;
            while (it1!=this->numbers.end() || it2!=b.numbers.end()) {
                if (it1 != this->numbers.end()) {
                    dif += *it1;
                    ++it1;
                }
                if (it2 != b.numbers.end()) {
                    dif -= *it2;
                    ++it2;
                }
                if (dif < 0) {
                    *(it1 - 1) = dif + this->base;
                    dif = -1;
                } else {
                    *(it1 - 1) = dif % this->base;
                    dif /= this->base;
                }
            }
            if (dif < 0)
                this->positive = false;

            if (this->numbers.size() > 1) {
                do {
                    it1 = this->numbers.end() - 1;
                    if (*it1 == 0)
                        this->numbers.pop_back();
                    else
                        break;
                } while (this->numbers.size() > 1);
            }
            return *this;
        }

        // Multiplication
        BigInteger operator*(BigInteger const &b) {
            if (b.numbers.size() == 1)
                return *this *= b.numbers[0];
            std::vector<int>::iterator it1;
            std::vector<int>::const_iterator it2;
            BigInteger c;
            for (it1=this->numbers.begin(); it1!=this->numbers.end(); ++it1) {
                for (it2=b.numbers.begin(); it2!=b.numbers.end(); ++it2) {
                    c.skip = (unsigned int) (it1 - this->numbers.begin()) + (it2 - b.numbers.begin()); // TODO
                    c += (long long) (*it1) * (*it2);
                }
            }
            c.skip = 0;
            return c;
        }

        BigInteger &operator*=(BigInteger const &b) {
            *this = *this * b;
            return *this;
        }

        BigInteger operator*(long long const &b) {
            *this = *this * b;
            return *this;
        }

        BigInteger &operator*=(int const &b) {
            std::vector<int>::iterator it = this->numbers.begin();
            long long sum = 0;
            while (it != numbers.end()) {
                sum += (long long) (*it) * b;
                *it = (int) (sum % this->base);
                sum /= this->base;
                ++it;
            }
            if (sum)
                this->numbers.push_back((int) sum);
            return *this;
        }

        // Compare
        bool operator<(const BigInteger &b) const {
            return this->compare(b) == -1;
        }

        bool operator>(const BigInteger &b) const {
            return this->compare(b) == 1;
        }

        bool operator<=(const BigInteger &b) const {
            return this->compare(b) != 1;
        }

        bool operator>=(const BigInteger &b) const {
            return this->compare(b) != -1;
        }

        bool operator==(const BigInteger &b) const {
            return this->compare(b) == 0;
        }

        bool operator!=(const BigInteger &b) const {
            // return ! (*this == b);
            return this->compare(b) != 0;
        }

        // Allocation
        BigInteger operator=(const long long &a) {
            this->numbers.clear();
            long long t = a;
            do {
                this->numbers.push_back((int) (t % this->base));
                t /= this->base;
            } while (t != 0);
            return *this;
        }

        // Access
        int operator[](int const &b) {
            return this->to_string()[b] - '0';
        }

        // Input & Output
        friend std::istream &operator>>(std::istream &in, BigInteger &a) {
            std::string str;
            in >> str;
            a = str;
            return in;
        }

        friend std::ostream &operator<<(std::ostream &out, BigInteger const &a) {
            if (!a.numbers.size())
                return out << 0;
            int i = a.numbers.size() - 1, len;
            for (; i>=0 && a.numbers[i]==0; --i);
            if (i == -1)
                return out << 0;
            if (!a.positive)
                out << '-';
            std::vector<int>::const_reverse_iterator it = a.numbers.rbegin() + (a.numbers.size() - i - 1);
            out << *it++;
            for (; it!=a.numbers.rend(); ++it) {
                for (i=0, len=a.segment_length(*it); i<9-len; ++i)
                    out << '0';
                if (*it)
                    out << *it;
            }
            return out;
        }

        // Helpers
        void clear() {
            this->numbers.clear();
            this->positive = true;
            this->skip = 0;
        }

        BigInteger &abs() {
            this->positive = true;
            return *this;
        }

        // Power
        BigInteger &pow(int const &power) {
            std::map<int, BigInteger> lookup;
            if (power%2==0 && !this->positive) {
                this->positive = true;
            }
            *this = this->pow(power, lookup);
            return *this;
        }

        // Trivia
        std::string to_string() {
            std::ostringstream stream;
            stream << *this;
            return stream.str();
        }

        int digits() const {
            int segments = this->numbers.size();
            if (segments == 0)
                return 0;
            int digits = 9 * (segments - 1);
            digits += segment_length(this->numbers.back());
            return digits;
        }

        int trailing_zeros() const {
            if (this->numbers.empty() || (this->numbers.size()==1 && this->numbers[0]==0))
                return 1;

            int zeros = 0;
            std::vector<int>::const_iterator it = this->numbers.begin();
            if (this->numbers.size() > 1) {
                for (; it!=this->numbers.end()-1 && *it==0; ++it) {
                    zeros += 9;
                }
            }
            int a = *it;
            while (a%10==0 && a) {
                ++zeros;
                a /= 10;
            }
            return zeros;
        }
};

BigInteger factorial(int n) {
    BigInteger result = 1;
    if (n % 2) {
        result = n;
        --n;
    }
    int last = 0;
    for (; n>=2; n-=2) {
        result *= n + last;
        last += n;
    }
    return result;
}
