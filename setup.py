from setuptools import setup, find_packages

setup(
    author="zhupr,gazh,you_N_G",
    author_email="zplongr@hotmail.com,v-gazh@hotmail.com",
    name="wan",
    version="0.0.2.dev0",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["wan=wan:run"],
    },
    install_requires=[
        "loguru",
        "notifiers",
        "fire",
        "psutil",
        "iterfzf",
        "PyYAML",
        "watchdog",
    ],
)
