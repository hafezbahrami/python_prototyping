
# 1 Compiling python code using Numba
**Numba** is an open-source JIT (Just-In-Time) compiler that translates a subset of Python and NumPy code into fast machine code using LLVM (Low-Level Virtual Machine). 
 
 #### 1-1 JIT Compilation
 Numba can compile Python functions at runtime to machine code, which can significantly improve execution speed.
 [example](./01_python_JIT_compilation.py) provided here shows how a simple loop for adding elements within an aray can significantly be faster by simply using runtime-compilation using JIT.