/*
 * @Time     : 2019/01/27 19:20
 * @Author   : Iydon
 * @File     : time.h 
 */

class Time {
    public:
        Time(int,int,int);
        void set_year(int);
        void set_day(int);
        void set_minute(int);
        int get_year(void) { return _year; }
        int get_day(void) { return _day; }
        int get_minute(void) { return _minute; }
        double double_in_years(void);
        double double_in_day(void);
    private:
        int _year, _day, _minute;
        int _YEAR2DAY   = 365;
        int _DAY2MINUTE = 60 * 24;
};

Time::Time(int year, int day, int minute) {
    _year   = year;
    _day    = day;
    _minute = minute;
}

void Time::set_year(int year) {
    _year = year;
}

void Time::set_day(int day) {
    _day = day;
}

void Time::set_minute(int minute) {
    _minute = minute;
}

double Time::double_in_years(void) {
    return (double)_year + double_in_day()/_YEAR2DAY;
}

double Time::double_in_day(void) {
    return (double)_day + (double)_minute/_DAY2MINUTE;
}
