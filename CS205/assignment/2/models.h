#pragma once


#include <iostream>
#include <map>
#include <cmath>
#include <regex>
#include <list>

#include "timer.h"


#define UF(o, s) this->unary_functions[#o] = [] (REAL number) -> REAL { s; };
#define UFD(o) UF(o, return o(number);)
#define BFD(o) BF(o, return left o right;)
#define BF(o, s) this->binary_functions[#o] = [] (REAL left, REAL right) -> REAL { s; };
#define VF(o, s) this->variable_functions[#o] = [this] (string key, REAL value) -> REAL { s; return this->variables[key]; };
#define VFD(o) VF(o, this->variables[key] o value;)


using namespace std;


struct token {
    enum TokenType {
        UNARY_FUNCTION, BINARY_FUNCTION, VARIABLE_FUNCTION, NUMBER, VARIABLE,
        LEFT_PARENTHESE, RIGHT_PARENTHESE, LEFT_BRACE, RIGHT_BRACE, EMPTY
    } type;
    string value;
};


template<class REAL = double, class INTEGER = int>
class Globals {
    /*
     * 全局变量与函数
     */
    public:
        // 变量定义
        map<string, function<REAL(REAL)>> unary_functions;
        map<string, function<REAL(REAL, REAL)>> binary_functions;
        map<string, function<REAL(string, REAL)>> variable_functions;
        map<string, REAL> variables;
        map<string, regex> patterns;

        // 构造器
        Globals () {
            this->initialize_functions();
            this->initialize_variables();
            this->initialize_patterns();
        }

        function<REAL(REAL)> get_unary_function(string key) {
            return this->unary_functions.at(key);
        }

        function<REAL(REAL, REAL)> get_binary_function(string key) {
            return this->binary_functions.at(key);
        }

        function<REAL(string, REAL)> get_variable_function(string key) {
            return this->variable_functions.at(key);
        }

    private:
        void initialize_functions() {
            // unary and binary functions
            UFD(+);UFD(-);UFD(!);UFD(cos);UFD(sin);UFD(tan);UFD(acos);UFD(asin);UFD(atan);UFD(cosh);UFD(sinh);UFD(tanh);UFD(acosh);UFD(asinh);UFD(atanh);UFD(exp);UFD(log2);UFD(log10);UFD(sqrt);UFD(erf);UFD(ceil);UFD(floor);UFD(round);UFD(abs);
            BFD(+);BFD(-);BFD(*);BFD(/);BFD(>);BFD(<);BFD(==);BFD(>=);BFD(<=);BFD(!=);BFD(||);BFD(&&);

            UF(ln, return log(number););
            UF(print, cout << number << endl; return number;)

            BF(%, return fmod(left, right););
            BF(^, return pow(left, right););
            BF(|, return (INTEGER)left | (INTEGER)right;);
            BF(&, return (INTEGER)left & (INTEGER)right;);

            // functions involving variables
            VFD(=);VFD(+=);VFD(-=);VFD(*=);VFD(/=);

            VF(%=, this->variables[key] = fmod(this->variables[key], value););
            VF(^=, this->variables[key] = pow(this->variables[key], value););
            VF(|=, this->variables[key] = (INTEGER)this->variables[key] | (INTEGER)value;);
            VF(&=, this->variables[key] = (INTEGER)this->variables[key] & (INTEGER)value;);
            VF(<<=, this->variables[key] = (INTEGER)this->variables[key] << (INTEGER)value;);
            VF(>>=, this->variables[key] = (INTEGER)this->variables[key] >> (INTEGER)value;);
        }

        void initialize_variables() {
            this->variables["pi"] = 3.14159265358979323846;
            this->variables["e"] = 2.71828182845904523536;
            this->variables["_"] = 0;
        }

        void initialize_patterns() {
            this->patterns["number"] = "([1-9]\\d*|0)(\\.\\d*)?([eE][+-]?([1-9]\\d*|0))?";
            this->patterns["comment"] = "#[^\\n]*";
            this->patterns["whitespace"] = "[ \\r\\t\\f\\v]+";
            this->patterns["breakline"] = "\\.\\.\\.\\n*";
            this->patterns["semicolon"] = ";";
        }
};


template<class REAL = double, class INTEGER = int>
class Interpreter {
    /*
     * 解释器
     */
    public:
        void run(string code) {
            this->timer.tic();
            list<string> lines = this->split_lines(
                this->remove_comment_whitespace_breakline(code)
            );
            for (auto &line : lines) {
                if (!this->command(line)) {
                    this->globals.variables["_"] = this->parse(
                        this->split_tokens(line)
                    );
                }
            }
            this->timer.toc();
            if (this->whether_to_time)
                this->timer.print();
        }

    private:
        Globals<REAL, INTEGER> globals;
        Timer timer;
        bool whether_to_time = false;

        string remove_comment_whitespace_breakline(string code) {
            return regex_replace(
                regex_replace(
                    regex_replace(
                        regex_replace(code, this->globals.patterns["comment"], ""),
                        this->globals.patterns["semicolon"], "\n"
                    ), this->globals.patterns["whitespace"], ""
                ), this->globals.patterns["breakline"], ""
            );
        }

        list<string> split_lines(string code) {
            list<string> result;
            if (code != "") {
                size_t pos, size = code.size();
                for (int ith=0; ith<size; ith++) {
                    pos = code.find("\n", ith);
                    if (pos<size && ith!=pos) {
                        result.push_back(code.substr(ith, pos-ith));
                        ith = pos;
                    }
                }
            }
            return result;
        }

        list<token> split_tokens(string line) {
            /*
             * 分离 token
             */
            list<token> result;
            int ith, jth, type;
            string name, segment;
            smatch match;
            // iteration
            for (ith=0; ith<line.size(); ith++) {
                // *_PARENTHESE, *_BRACE
                if (line[ith] == '(') {
                    result.push_back({token::LEFT_PARENTHESE, "("});
                } else if (line[ith] == ')') {
                    result.push_back({token::RIGHT_PARENTHESE, ")"});
                } else if (line[ith] == '{') {
                    result.push_back({token::LEFT_BRACE, "{"});
                } else if (line[ith] == '}') {
                    result.push_back({token::RIGHT_BRACE, "}"});
                } else {
                    // *_FUNCTION
                    name = "";
                    for (jth=ith; jth<line.size(); jth++) {
                        segment = line.substr(ith, jth-ith+1);
                        if (this->globals.unary_functions.count(segment))
                            type = token::UNARY_FUNCTION;
                        else if (this->globals.binary_functions.count(segment))
                            type = token::BINARY_FUNCTION;
                        else if (this->globals.variable_functions.count(segment))
                            type = token::VARIABLE_FUNCTION;
                        else continue;
                        name = segment;
                    }
                    if (!name.empty()) {
                        ith += name.size() - 1;
                        result.push_back({(token::TokenType)type, name});
                    // NUMBER
                    } else if ('0'<=line[ith] && line[ith]<='9') {
                        segment = line.substr(ith, line.size()-ith);
                        regex_search(segment, match, this->globals.patterns["number"]);
                        result.push_back({token::NUMBER, match[0]});
                        ith += match.length(0) - 1;
                    // VARIABLE
                    } else {
                        if (result.size() && result.back().type==token::VARIABLE)
                            result.back().value += line[ith];
                        else
                            result.push_back({token::VARIABLE, line.substr(ith, 1)});
                    }
                }
            }
            return result;
        }

        REAL parse(list<token> tokens) {
            /*
             * 根据 token 得出结果
             */
            int stack = 0;
            REAL result;
            list<token> priority;
            list<token>::iterator it, begin, end, medium;
            // 去除优先项
            for (it=tokens.begin(); it!=tokens.end(); it++) {
                if ((*it).type == token::LEFT_BRACE) {
                    if (stack == 0)
                        begin = it;
                    stack += 1;
                } else if ((*it).type == token::RIGHT_BRACE) {
                    stack -= 1;
                    if (stack == 0) {
                        end = it;
                        priority.assign(++begin, end);
                        *(--begin) = {token::NUMBER, to_string(this->parse(priority))};
                        for (medium=(++begin), end++; medium!=end; medium++)
                            *medium = {token::EMPTY, ""};
                    }
                }
            }
            tokens.remove_if([] (token t) -> bool { return t.type==token::EMPTY; });
            // 去除函数项
            for (it=tokens.begin(); it!=tokens.end(); it++) {
                if ((*it).type == token::LEFT_PARENTHESE) {
                    if (stack == 0)
                        begin = it;
                    stack += 1;
                } else if ((*it).type == token::RIGHT_PARENTHESE) {
                    stack -= 1;
                    if (stack == 0) {
                        end = it;
                        priority.assign(++begin, end);
                        begin--; begin--;
                        result = this->globals.unary_functions[(*begin).value](this->parse(priority));
                        *begin = {token::NUMBER, to_string(result)};
                        for (medium=++begin, end++; medium!=end; medium++)
                            *medium = {token::EMPTY, ""};
                    }
                }
            }
            tokens.remove_if([] (token t) -> bool { return t.type==token::EMPTY; });
            // 无优先级无显性函数调用表达式解析
            return this->parse_arithmetic(tokens);
        }

        REAL parse_arithmetic(list<token> tokens) {
            /*
             * 无优先级无显性函数调用表达式的解析
             */
            REAL result;
            token previous;
            list<token>::iterator it = tokens.begin();
            // 递归结束条件
            if (tokens.size() == 1)
                return this->to_real(tokens.front());
            // 递归状态
            switch (it->type) {
                case token::NUMBER:
                case token::VARIABLE: {
                    previous = *it;
                    switch ((++it)->type) {
                        case token::UNARY_FUNCTION:
                        case token::BINARY_FUNCTION: {
                            result = this->globals.binary_functions[it->value](
                                this->to_real(previous), this->to_real(*(++it))
                            );
                            *it = {token::NUMBER, to_string(result)};
                            tokens.pop_front(); tokens.pop_front();
                            return this->parse_arithmetic(tokens);
                        }

                        case token::VARIABLE_FUNCTION: {
                            result = this->globals.variable_functions[it->value](
                                previous.value, this->to_real(*(++it))
                            );
                            *it = {token::NUMBER, to_string(result)};
                            tokens.pop_front(); tokens.pop_front();
                            return this->parse_arithmetic(tokens);
                        }
                    }
                }

                case token::UNARY_FUNCTION: {
                    result = this->globals.unary_functions[it->value](this->to_real(*(++it)));
                    *it = {token::NUMBER, to_string(result)};
                    tokens.pop_front();
                    return this->parse_arithmetic(tokens);
                }
            }
            return 0;
        }

        REAL to_real(token t) {
            switch (t.type) {
                case token::NUMBER:
                    return stold(t.value);

                case token::VARIABLE:
                    return this->globals.variables[t.value];

                default:
                    return 0;
            }
        }

        void print(list<token> tokens) {
            /*
             * 用于 debug 输出信息
             */
            string names[] = {
                "UNARY_FUNCTION", "BINARY_FUNCTION", "VARIABLE_FUNCTION", "NUMBER", "VARIABLE",
                "LEFT_PARENTHESE", "RIGHT_PARENTHESE", "LEFT_BRACE", "RIGHT_BRACE", "EMPTY"
            };
            for (auto &t : tokens)
                cout << t.value << "(" << names[t.type] << ")" << " ";
            cout << endl;
        }

        template<typename K, typename V>
        void print(map<K, V> dict, string prefix="", string suffix="\n") {
            for (typename map<K, V>::iterator it=dict.begin(); it!=dict.end(); it++) {
                cout << prefix << it->first << ": " << it->second << suffix;
            }
        }

        bool command(string line) {
            if (line == "variables") {
                cout << "{" << endl;
                this->print<string, REAL>(this->globals.variables, "    ", ",\n");
                cout <<"}" << endl;
            } else if (line == "functions") {
                cout << "Unary functions:\n    ";
                for (auto item : this->globals.unary_functions)
                    cout << item.first << ", ";
                cout << endl << endl;
                cout << "Binary functions:\n    ";
                for (auto item : this->globals.binary_functions)
                    cout << item.first << ", ";
                cout << endl << endl;
                cout << "Variable functions:\n    ";
                for (auto item : this->globals.variable_functions)
                    cout << item.first << ", ";
                cout << endl << endl;
            } else if (line == "timeon") {
                this->whether_to_time = true;
            } else if (line == "timeoff") {
                this->whether_to_time = false;
            } else
                return false;
            return true;
        }
};
