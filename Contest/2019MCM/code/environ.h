/*
 * @Time     : 2019/01/25 13:10
 * @Author   : Iydon
 * @File     : environ.h 
 */

#include <stdio.h>


class Environ {
    public:
        /* functions */
        Environ(int);
        void set_attributions(double,double,double);
        void set_temperature(double);
        void set_humidity(double);
        void set_energy_dens(double);
        void add_temperature(double);
        void add_humidity(double);
        void add_energy_dens(double);
        double get_temperature(void){ return _temperature; }
        double get_humidity(void){ return _humidity; }
        double get_energy_dens(void){ return _energy_dens; }
        void print_info(void);
        /* interface */
        void simulate(Time);
        /* rules */ 
    private:
        /* attributions */
        unsigned int _id    = 0;
        bool   _display     = true;
        double _temperature = 0.0;
        double _humidity    = 0.0;
        double _energy_dens = 0.0;
        /* part constant */
        double _period = 1.0;
};

Environ::Environ(int id) {
    _id = id;
}

void Environ::set_attributions(double temperature, double humidity, double energy_dens) {
    _temperature = temperature;
    _humidity    = humidity;
    _energy_dens = energy_dens;
    print_info();
}

void Environ::set_temperature(double value) {
    _temperature = value;
    if (_temperature<-273.15) _temperature=-273.15;
}

void Environ::set_humidity(double value) {
    _humidity = value;
    if (_humidity<0.0) _humidity=0.0;
    else if (_humidity>1.0) _humidity=1.0;
}

void Environ::set_energy_dens(double value) {
    _energy_dens = value;
    if (_energy_dens<0.0) _energy_dens=0.0;
}

void Environ::add_temperature(double value) {
    _temperature += value;
    if (_temperature<-273.15) _temperature=-273.15;
}

void Environ::add_humidity(double value) {
    _humidity += value;
    if (_humidity<0.0) _humidity=0.0;
    else if (_humidity>1.0) _humidity=1.0;
}

void Environ::add_energy_dens(double value) {
    _energy_dens += value;
    if (_energy_dens<0.0) _energy_dens=0.0;
}

void Environ::print_info(void) {
    if (_display) {
        printf("%10s: %10x\n", "ID", _id);
        printf("%10s: %10.3f ℃\n", "Tempature", _temperature);
        printf("%10s: %10.3f %%\n", "Humidity", _humidity*100);
        printf("%10s: %10.3f kJ/m²\n", "Energy ρ", _energy_dens);
        printf("\n");
    }
}
