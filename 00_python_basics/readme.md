# 1 private method in python
There is nothing as private and secure method in Python ([Example](./00_private_method_in_python.py.py)).
- Direct access tp private method or attribute is **not possible**. This will raise in "AttributeError"
- However, Private methods and attributes can still be accessed from outside the class using name mangling. The name is mangled to _ClassName__methodName or _ClassName__attributeName.

# 2 Python being patchable
- Python's dynamic nature allows it to be highly flexible and patchable. 
- This means that you can modify objects, functions, and even classes at runtime. This can be particularly useful for tasks such as monkey patching, where you modify or extend the behavior of libraries or classes without altering the original source code.
[Example](./01_patchable_python.py) is provided here.

# 3 Python with "Introspection functions"
- Python introspection is the ability of a program to examine the type or properties of an object at runtime.
- It allows you to inspect various aspects of your code, such as modules, classes, functions, and methods, as well as retrieve information about their attributes and methods.
- This feature makes Python a highly dynamic and flexible language.

How does introspection works in pratice:
- **Without using inspect library**:
    - We most useful command is: $dir(myObj)$ or equivalently "myObj.__dir__()". It will list all the methods and attributes that it sposes for exploring the class and object.
    - hasattr(obj, 'value')  &&&  getattr(obj, 'value')   &&&    setattr(obj, 'value', 20)
    - On documentations: MyClass.__doc__     &&&      example_function.__name__

- **Using inspect library**:
    - all the methods in a class: inspect.getmembers(MyClass, inspect.isfunction)
    - docs: inspect.getdoc(MyClass)     &&&   
    - Info about the input and signiture of a method within a class:  inspect.signature(MyClass.method)
