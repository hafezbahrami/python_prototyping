// We just need to run the below command in command-line
//         python setup.py build

// Reference:   https://www.youtube.com/watch?v=a65JdvOaygM&t=1156s&ab_channel=DrapsTV
//              https://tutorialedge.net/python/python-c-extensions-tutorial/

// A dumb Module to calculate the Fibbonacci number in C to make it faster!

#include <Python.h>

// ------------------------------------------------------------------------------------------------------------------
// (1) A simple C function that we want to call it from Python to make computation faster
// ------------------------------------------------------------------------------------------------------------------
int Cfib(int n)
{
    if (n < 2)
        return n;
    else
        return Cfib(n-1)+Cfib(n-2);
}

// ------------------------------------------------------------------------------------------------------------------
// (2) The main wrapper for our C function
// ------------------------------------------------------------------------------------------------------------------

// This method recieves some PyThon Object, also some args in PythonObject, and at the end returns some PythonObject
static PyObject *fib(PyObject *self, PyObject *args)

{
    // Instantiate our n value
    int n; // Local variable n, to store an incoming value from Python
    // if statement, for error checking ==> PyArg_ParseTuple will parse sTuples from Python to C  ==> passging the args from 
    // Python that comes through, then we want to grab "integer" ("int") out of it, then we want to place that integer 
    // into "&n" [a variable that we just created above]   ==> If that initeger variable is not in the args passed by Python, return NULL
    if(!PyArg_ParseTuple(args, "i", &n)) 
        return NULL;

    // At this point, we are sure that our integer successfully stored in "n"
    // Py_BuildValue  ==> Will make sure to turn a C value to a Python Value (which is consistent with the return type of this -->   static PyObject *fib( .... )  )
    return Py_BuildValue("i", Cfib(n));
}

// There is no arg for the method below
static PyObject *version(PyObject *self){
    // We want to reurn a PyObject, "s" means we want to return a string. Ans the string that we want to return as PytObject is "Version 0.01".
    return Py_BuildValue("s", "Version 0.01");
}


// ------------------------------------------------------------------------------------------------------------------
// (3) Our module's function definition struct  --> We require this "Null" to signal the end of our method
// ------------------------------------------------------------------------------------------------------------------
// {"function_in_Python",    wrapper_function_here,      arguments,     "some_descriptions"}
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
