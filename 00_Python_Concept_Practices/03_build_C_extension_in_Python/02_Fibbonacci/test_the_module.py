# Make sure we ran the "python setup.py build", in order to get the *.so file for our package.
# Then, we need to make sure to copy the *.so file here, so we can import it

# Reference: https://www.youtube.com/watch?v=a65JdvOaygM&t=1156s&ab_channel=DrapsTV

import myDumbModule

n = 10
fib_num = myDumbModule.fib(n)
print(f"The Fibbonacci number({n}) is {fib_num}")
print(f"The Version of my Dumb Extension is {myDumbModule.version()}")