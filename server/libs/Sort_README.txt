the sort.py file is an open source implementation of the SORT algorithm.

The open source project is here:
    https://github.com/abewley/sort

The SORT paper is here:
    https://arxiv.org/pdf/1602.00763.pdf

Because of a problem compiling a Python prerequisite (Numba) we made a minor
modification to the open source implementation:
    - Commented out the 'import numba' line
    - Commented out the @jit decorator 

For future reference: a potentially improved implementation is here:
    https://github.com/nwojke/deep_sort
