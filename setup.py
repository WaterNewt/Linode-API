from setuptools import setup, find_packages

setup(
    name='mylinode-api',
    description="A module to simplify Linode interactions.",
    author_email="waternewtinfo@gmail.com",
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['requests'],
)