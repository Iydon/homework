#include <Python.h>
#include "plot_utils.h"
#include "plot_utils.c"

void plot(double *x, double *y, int length, const char* name) {
    Py_Initialize();
    PyInit_plot_utils();

    PyObject *_x = PyList_New(length);
    PyObject *_y = PyList_New(length);

    for (int i=0; i<length; i++) {
        PyList_SetItem(_x, i, PyFloat_FromDouble(x[i]));
        PyList_SetItem(_y, i, PyFloat_FromDouble(y[i]));
    }

    plot(_x, _y, PyUnicode_FromString(name));

    Py_Finalize();
}

void loglog(double *x, double *y, int length, const char* name) {
    Py_Initialize();
    PyInit_plot_utils();

    PyObject *_x = PyList_New(length);
    PyObject *_y = PyList_New(length);

    for (int i=0; i<length; i++) {
        PyList_SetItem(_x, i, PyFloat_FromDouble(x[i]));
        PyList_SetItem(_y, i, PyFloat_FromDouble(y[i]));
    }

    loglog(_x, _y, PyUnicode_FromString(name));

    Py_Finalize();
}
