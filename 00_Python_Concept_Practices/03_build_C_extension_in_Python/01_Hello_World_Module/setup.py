# We just need to run the below command in command-line
#                 python setup.py build

from distutils.core import setup, Extension

module = Extension("myDumbModule", sources=["hello_world.c"])

setup(name="myFakePackage",
      version="0.01",
      description="This is the example module we created for C",
      ext_modules=[module])