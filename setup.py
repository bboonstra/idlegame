from setuptools import setup, find_packages

setup(
    name='idlegame',
    version='1.6.2.1',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'idlegame=idlegame.main:main',  # Existing entry point
        ],
        'gui_scripts': [  # This line enables running via python command
            'idlegame=idlegame.main:main',
        ],
    },
    description='A tiny idle game you can play right from your terminal, if you are bored at your software development job',
    author='Ben Boonstra',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
)
