from setuptools import setup, find_packages

setup(
    name='mylinode_api',
    description="A module to simplify Linode interactions.",
    long_description=open("README.md", "r").read(),
    author="Yunus Ruzmetov",
    author_email="waternewtinfo@gmail.com",
    url="https://github.com/WaterNewt/Linode-API",
    download_url="https://github.com/WaterNewt/Linode-API/releases/tag/v1.0.0",
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['requests'],
)