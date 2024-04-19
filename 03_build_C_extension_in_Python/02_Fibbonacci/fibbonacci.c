// We just need to run the below command in command-line
//         python setup.py build

// Reference: https://tutorialedge.net/python/python-c-extensions-tutorial/

// A dumb Module to calculate the Fibbonacci number in C to make it faster!

#include <Python.h>


int Cfib(int n)
{
    if (n < 2)
        return n;
    else
        return Cfib(n-1)+Cfib(n-2);
}

//Creating our PyObject  (following Python standard on what to put in input argumets)
static PyObject *fib(PyObject *self, PyObject *args)
{
    // Instantiate our n value
    int n;
    // if our n value
    if(!PyArg_ParseTuple(args, "i", &n))
        return NULL;

    // return our computed fibbonacci number
    return Py_BuildValue("i", Cfib(n));
}


static PyObject *version(PyObject *self){
    return Py_BuildValue("s", "Version 0.01");
}


// Our module's function definition struct
// We require this "Null" to signal the end of our method
// Definition
static PyMethodDef myDumbMethods[] = {
    {"fib", fib, METH_VARARGS, "Some Description Here: A dumb Module to calculate the Fibbonacci number in C to make it faster!"},
    {"version", (PyCFunction)version, METH_NOARGS, "return the version of the module"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef myDumbModule = {
    PyModuleDef_HEAD_INIT,
    "myDumbModule",
    "A dumb Module to calculate the Fibbonacci number in C to make it faster!",
    -1, // global state
    myDumbMethods
};

// Initialize the function
PyMODINIT_FUNC PyInit_myDumbModule(void)
{
    return PyModule_Create(&myDumbModule);
}
