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
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
