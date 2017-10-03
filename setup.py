from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'doing away with defaults',
  ext_modules = cythonize("main.pyx"),
)
