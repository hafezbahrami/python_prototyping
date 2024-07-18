class MyClass:
    def __init__(self):
        self.__private_attribute = "I am private"

    def __private_method(self):
        print("This is a private method")

    def public_method(self):
        print("This is a public method")
        self.__private_method()
        print(self.__private_attribute)

# Create an instance of the class
obj = MyClass()

# Call the public method
obj.public_method()

# -----------------------------------------------------------------------------------------------------
# (1) Trying to directly access the private method or attribute directly will raise an AttributeError
try:
    obj.__private_method()
except AttributeError as e:
    print(e)

try:
    print(obj.__private_attribute)
except AttributeError as e:
    print(e)

# -----------------------------------------------------------------------------------------------------
# (2) Accessing the private method or attribute via name mangling: Private methods and attributes can 
# still be accessed from outside the class using name mangling. The name is mangled 
# to _ClassName__methodName or _ClassName__attributeName.
obj._MyClass__private_method()
print(obj._MyClass__private_attribute)
