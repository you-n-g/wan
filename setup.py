from setuptools import setup, find_packages
setup(
    author = 'zhupr',
    author_email = 'zplongr@hotmail.com',
    name='wan',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['wan=wan:run'],
    },
    install_requires=[
        'loguru>=0.5.1',
        'notifiers>=1.2.1',
        'fire>=0.3.1',
        'psutil>=5.7.0',
        'iterfzf>=0.5.0.20.0',
    ],
)
