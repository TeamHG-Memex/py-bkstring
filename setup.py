from distutils.core import setup, Extension

setup(name = 'bkstring',
    version = '0.0.1',
    description = 'Python wrapper for the bk-string C library.',
    author = 'Brian Mackintosh',
    author_email = 'bcmackintosh@gmail.com',
    url = 'github.com/bcmackintosh/py-bkstring',
    packages = ['bkstring'],
    package_dir = {'bkstring': 'lib'},
    package_data = {'bkstring': ['shared/libbkstring.so']})
