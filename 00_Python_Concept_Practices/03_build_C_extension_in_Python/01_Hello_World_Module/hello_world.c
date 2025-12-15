// We just need to run the below command in command-line
//         python setup.py build

// Reference: https://tutorialedge.net/python/python-c-extensions-tutorial/

#include <Python.h>


//Creating our PyObject  (following Python standard on what to put in input argumets)
static PyObject *helloWorld(PyObject *self, PyObject *args){
   printf("Hello World, from C-extension of Python!");
    return Py_None;
}


static PyObject *version(PyObject *self){
    return Py_BuildValue("s", "Version 0.01");
}


// Our module's function definition struct
// We require this "Null" to signal the end of our method
// Definition
static PyMethodDef myDumbMethods[] = {
    {"helloWorld", helloWorld, METH_VARARGS, "Some Description Here: Say Hello to the World"},
    {"version", (PyCFunction)version, METH_NOARGS, "return the version of the module"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef myDumbModule = {
    PyModuleDef_HEAD_INIT,
    "myDumbModule",
    "say hello to the worls to test the Module",
    -1, // global state
    myDumbMethods
};

// Initialize the function
PyMODINIT_FUNC PyInit_myDumbModule(void)
{
    return PyModule_Create(&myDumbModule);
}
