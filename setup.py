from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np
import os,cython


sourcefiles = ['floyd.pyx']
this_dir = os.path.split(cython.__file__)[0]
extensions = [
    Extension("floyd", sourcefiles,
              include_dirs=[np.get_include(),this_dir])
    ]

setup(cmdclass={'build_ext': build_ext},
      ext_modules=extensions)