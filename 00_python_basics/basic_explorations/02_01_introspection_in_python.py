import inspect

class MyClass:
    """This is a sample class for introspection."""
    
    def __init__(self, value):
        self.value = value
    
    def method(self):
        """This is a sample method."""
        return self.value

def example_function():
    """This is a sample function."""
    pass

# Using type and isinstance
obj = MyClass(10)
print(type(obj))  # Output: <class '__main__.MyClass'>
print(isinstance(obj, MyClass))  # Output: True

# Using dir: Lists the attributes and methods of an object.
print(dir(obj))

# Using help
# help(obj)

# Using getattr, setattr, hasattr
print(getattr(obj, 'value'))  # Output: 10
setattr(obj, 'value', 20)
print(obj.value)  # Output: 20
print(hasattr(obj, 'value'))  # Output: True

# Using __doc__ and __name__
print(MyClass.__doc__)  # Output: This is a sample class for introspection.
print(example_function.__name__)  # Output: example_function

# Using inspect module
print(inspect.getmembers(MyClass, inspect.isfunction))
# Output: [('method', <function MyClass.method at 0x...>)]
print(inspect.getdoc(MyClass))
# Output: This is a sample class for introspection.
print(inspect.signature(MyClass.method))
# Output: (self)
