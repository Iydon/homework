/*
 * @Time     : 2019/01/25 13:18
 * @Author   : Iydon
 * @File     : interface.h 
 */

#include <random>
#include <math.h>

using namespace std;


std::default_random_engine e;


/*
 * Dragon.
 */
void Dragon::simulate(double inc, Time time, Environ envir) {
    grow_up(time, inc);
    move_on(time, envir);
}

 void Dragon::grow_up(Time time, double inc) {
    /*
     * time, spirit, energy.
     */
    _age += inc;
    if (time.get_minute()==0) {
        add_weight(-7500.0/(1+596.0*exp(-_age))+7500.0/(1+596.0*exp(-_age-1.0/365)));
    }
    if (_is_sleeping==0) {
        set_spirit(0.970284649/(1.0+0.000000098*exp((double)time.get_minute()/60)));
    }
    /* unsolved */
    lognormal_distribution<> ln_v(-_age*10000, 0.01);
    lognormal_distribution<> ln_e(-_age, 1);
    add_v(ln_v(e)/50);
    add_energy(ln_e(e));
    _max_energ = _energy;
 }

 void Dragon::move_on(Time time, Environ env) {
    /*
     * hunting, sleeping, flying, free.
     */
    if (_is_free==0) {
        if (_is_flying) flying(time, env);
        else if (_is_hunting) hunting(time, env);
        else if (_is_sleeping) sleeping(time, env);
        else set_status(0, free(time, env)+1);
        return;
    }
    uniform_real_distribution<> u(0, 1);
    if (_spirit<0.13) {
        set_status(3, sleeping(time, env)+1);
        return;
    }
    if (_energy<10.0) {
        set_status(2, hunting(time, env)+1);
        return;
    }
    if (u(e)<0.7) {
        set_status(1, flying(time, env)+1);
        return;
    }
    free(time, env);
 }

 int Dragon::free(Time time, Environ env) {
    _count_free += 1;
    _is_free -= 1;
    return 10;
 }

 int Dragon::flying(Time time, Environ env) {
    /*
     * ed:
     *     None.
     * ing:
     *     energy, spirit.
     */
    _count_flying += 1;
    _is_flying -= 1;
    uniform_real_distribution<> u(-1, 1);
    add_x(u(e)*_v);
    add_y(u(e)*_v);
    add_weight(-_v/10);
    add_energy(-_v);
    add_spirit(-1.0/_v);
    return 10;
 }

 int Dragon::hunting(Time time, Environ env) {
    /*
     * ed:
     *     energy.
     * ing:
     *     weight, spirit, energy.
     */
    _count_hunting += 1;
    _is_hunting -= 1;
    add_weight(_max_energ/10000);
    set_energy(_max_energ);
    add_spirit(-1.0/_v);
    return 10;
 }

 int Dragon::sleeping(Time time, Environ env) {
    /*
     * ed:
     *     spirit.
     * ing:
     *     spirit.
     */
    uniform_int_distribution<> u(-60,60);
    _count_sleeping += 1;
    _is_sleeping -= 1;
    add_spirit(0.001077);
    return 720 + u(e);
 }

void interaction(Dragon dragon) {
    /* too ugly to show */
}

double Dragon::satisf_index(Environ env) {
    return env.get_energy_dens()
         - abs(env.get_temperature()-27.0)
         - 10*abs(env.get_humidity()-0.7);
}


/*
 * Environment.
 */
void Environ::simulate(Time time) {
    normal_distribution<> n_t(0, 0.1);
    normal_distribution<> n_h(0, 0.001);
    normal_distribution<> n_e(0, 1);
    add_temperature(0.01*sin(2*3.1415927*time.double_in_years()) + n_t(e));
    add_humidity(n_h(e));
    if (_temperature>30.0) {
        add_energy_dens(10.0 + n_e(e));
    }
    if (_humidity>0.5) {
        add_energy_dens(10.0 + n_e(e));
    }
}
