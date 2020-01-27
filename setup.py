from setuptools import setup

setup(
    name='iliad-payment',
    version='0.0.1',
    description='Iliad payment solution',
    license='MIT',
    packages=['iliad_payment'],
    author='Joel Da Silva',
    author_email='jdasilva@corp.free.fr',
    keywords=['payments', 'payment solution'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
