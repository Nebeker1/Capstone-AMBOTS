from setuptools import setup, find_packages

setup(
    name='Capstone_AMBOTS2024',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
				'matplotlib',
				'numpy',
				'pandas',
				'datetime'
    ],
)