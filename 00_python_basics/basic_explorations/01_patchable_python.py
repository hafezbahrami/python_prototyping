"""
Python's dynamic nature allows it to be highly flexible and patchable. This means that you can modify objects, functions, and 
even classes at runtime. This can be particularly useful for tasks such as monkey patching, where you modify or extend the 
behavior of libraries or classes without altering the original source code.
"""


# Original class definition
class MyClass:
    def greet(self):
        return "Hello, world!"

# Create an instance of the class
obj = MyClass()
print(obj.greet())  # Output: Hello, world!

# Define a new method
def new_greet(self):
    return "Hello, universe!"

# Patch the method: MyClass.greet is patched by assigning the new_greet function to it. This effectively replaces the original greet method in the class.
MyClass.greet = new_greet

# Create a new instance of the class
new_obj = MyClass()
print(new_obj.greet())  # Output: Hello, universe!

# The original instance will also use the patched method
print(obj.greet())  # Output: Hello, universe!

