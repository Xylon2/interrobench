from setuptools import setup, find_packages

setup(
    name='interrobench',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'interrobench=interrobench.main:main',
        ],
    },
)