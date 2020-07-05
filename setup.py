from setuptools import setup, find_packages
setup(
    name='mytools',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['ntf=ntf:run'],
    },
    install_requires=[
        'loguru>=0.5.1',
        'notifiers>=1.2.1',
        'fire>=0.3.1',
    ],
)
