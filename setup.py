
from os import path
from setuptools import find_packages, setup

py_min = 6
py_max = 10
version = '0.0.7'

current_dir = path.dirname(path.abspath(__file__))

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

for index in range(py_min, py_max + 1):
    classifiers.append('Programming Language :: Python :: 3.%d' % index)


# Version management
version_path = path.join(current_dir, 'iliad_payment', 'version.py')

with open(version_path, 'w', encoding='utf8') as f:
    f.write('__version__ = \'%s\'\n' % version)


# Add a long description
readme_path = path.join(path.dirname(path.abspath(__file__)), 'README.md')
long_desc = None

with open(readme_path, 'r', encoding='utf8') as f:
    long_desc = f.read()


setup(
    name='iliad-payment',
    version=version,
    description='Iliad payment solution',
    license='MIT',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    author='Joel Da Silva',
    author_email='jdasilva@corp.free.fr',
    keywords=[
        'payments',
        'payment solution',
        'payment gateway',
        'credit cards',
        'sepa',
    ],
    install_requires=[
        'requests',
    ],
    python_requires=">=3.6",
    classifiers=classifiers,
)
