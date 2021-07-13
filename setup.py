
from os import path
from setuptools import find_packages, setup


# Import version
exec(open('iliad_payment/version.py').read())

# Add a long description
readme_path = path.join(path.dirname(path.abspath(__file__)), 'README.md')
long_desc = None

with open(readme_path, 'r', encoding='utf8') as f:
    long_desc = f.read()


setup(
    name='iliad-payment',
    version=__version__,
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
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
