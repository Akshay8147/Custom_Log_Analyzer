from setuptools import setup, Extension
import numpy

setup(
    name='pandas_c_extension',
    version='1.0',
    description='A C extension project using Pandas and NumPy',
    author='Your Name',
    author_email='your.email@example.com',
    install_requires=[
        'pandas>=1.0.0',
    ],
    ext_modules=[
        Extension(
            'extension_module',  # Your extension module name
            sources=['extension_source.c'],  # C source files
            include_dirs=[numpy.get_include()],  # Include NumPy headers
        )
    ],
    packages=['your_package_name'],  # Replace with your actual package name
)