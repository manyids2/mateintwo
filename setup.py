from setuptools import setup

setup(
    name='mateintwo',
    version='0.1',
    description='The mate in two trainer - Lazlo Polgar',
    url='http://github.com/manyids2/mateintwo',
    author='F T Horde',
    author_email='manyids2@gmail.com',
    license='MIT',
    packages=['mateintwo'],
    install_requires=[
        'python-chess',
        'termcolor',
        'pandas',
        'prompt_toolkit',
    ],
    zip_safe=False)
