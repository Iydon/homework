/*
 * @Time     : 2019/01/25 13:10
 * @Author   : Iydon
 * @File     : dragon.h 
 */

#include <stdio.h>


class Dragon {
    public:
        /* functions */
        Dragon(int);
        void set_attributions(double,bool,double,double,double,double,double,double);
        void set_weight(double);
        void set_energy(double);
        void set_spirit(double);
        void set_x(double);
        void set_y(double);
        void set_v(double);
        void add_weight(double);
        void add_energy(double);
        void add_spirit(double);
        void add_x(double);
        void add_y(double);
        void add_v(double);
        void print_info(void);
        double get_weight(void) { return _weight; }
        double get_energy(void) { return _energy; }
        double get_spirit(void) { return _spirit; }
        double get_x(void) { return _x; }
        double get_y(void) { return _y; }
        /* interface */
        void simulate(double,Time,Environ);
        void grow_up(Time,double);
        void move_on(Time,Environ);
        void set_status(int,int);
        int free(Time,Environ);
        int flying(Time,Environ);
        int hunting(Time,Environ);
        int sleeping(Time,Environ);
        void interaction(Dragon);
        double satisf_index(Environ);
    private:
        /* attributions */
        unsigned int _id  = 0;
        double _age       = 0;
        bool   _sex       = true;
        double _weight    = 10.0;
        double _energy    = 10.0;
        double _spirit    = 1.0;
        double _x=0.0, _y=0.0, _v=1.0;
        /* part constant */
        double _max_energ = _energy;
        /* flag */
        unsigned int _is_free     = 1;  
        unsigned int _is_flying   = 0;
        unsigned int _is_hunting  = 0;
        unsigned int _is_sleeping = 0;
        /* count */
        unsigned long int _count_free     = 0;
        unsigned long int _count_flying   = 0;
        unsigned long int _count_hunting  = 0;
        unsigned long int _count_sleeping = 0;
};

Dragon::Dragon(int id) {
    _id = id;
}

void Dragon::set_attributions(double age, bool sex, double weight, double energy,
                              double spirit, double x, double y, double v) {
    _age    = age;
    _sex    = sex;
    _weight = weight;
    _energy = energy;
    _spirit = spirit;
    _x      = x;
    _y      = y;
    _v      = v;
    print_info();
}

void Dragon::set_weight(double value) {
    _weight = value;
    if (_weight<0.0) _weight=0.0;
}

void Dragon::set_energy(double value) {
    _energy = value;
    if (_energy<0.0) _energy=0.0;
}

void Dragon::set_spirit(double value) {
    _spirit = value;
    if (_spirit<0.0) _spirit=0.0;
    else if (_spirit>1.0) _spirit=1.0;
}

void Dragon::set_x(double value) {
    _x = value;
}

void Dragon::set_y(double value) {
    _y = value;
}

void Dragon::set_v(double value) {
    _v = value;
    if (_v<0.0) _v=0.0;
}

void Dragon::add_weight(double value) {
    _weight += value;
    if (_weight<0.0) _weight=0.0;
}

void Dragon::add_energy(double value) {
    _energy += value;
    if (_energy<0.0) _energy=0.0;
}

void Dragon::add_spirit(double value) {
    _spirit += value;
    if (_spirit<0.0) _spirit=0.0;
    else if (_spirit>1.0) _spirit=1.0;
}

void Dragon::add_x(double value) {
    _x += value;
}

void Dragon::add_y(double value) {
    _y += value;
}

void Dragon::add_v(double value) {
    _v += value;
    if (_v<0.0) _v=0.0;
}

void Dragon::set_status(int status, int num) {
    /*
     * 0: Free. 
     * 1: Flying.
     * 2: Hunting.
     * 3: Sleeping.
     */
    _is_free     = 0;
    _is_flying   = 0;
    _is_hunting  = 0;
    _is_sleeping = 0;
    switch (status) {
        case 0: {
            _is_free = num;
            break;
        }
        case 1: {
            _is_flying = num;
            break;
        }
        case 2: {
            _is_hunting = num;
            break;
        }
        case 3: {
            _is_sleeping = num;
            break;
        }
    }
}

void Dragon::print_info(void) {
    printf("%10s: %10x\n", "ID", _id);
    printf("%10s: %10.1f year(s)\n", "Age", _age);
    printf("%10s: %10s\n", "Sex", _sex?"Male":"Female");
    printf("%10s: %10.1f kg\n", "Weight", _weight);
    printf("%10s: %10.1f kJ\n", "Energy", _energy);
    printf("%10s: %10.1f %%\n", "Spirit", _spirit*100);
    printf("%10s: %10.1f km\n", "Coor X", _x);
    printf("%10s: %10.1f km\n", "Coor Y", _y);
    printf("%10s: %10.1f km/min\n", "Velocity", _v);
    printf("%10s: %10.1f km/h\n", "Velocity", _v*60);
    printf("\n");
    printf("%10s %10lu minute(s)\n", "Free", _count_free);
    printf("%10s %10lu minute(s)\n", "Flying", _count_flying);
    printf("%10s %10lu minute(s)\n", "Hunting", _count_hunting);
    printf("%10s %10lu minute(s)\n", "Sleeping", _count_sleeping);
    printf("\n");
}
