from setuptools import setup, find_packages

setup(
    name='mylinode_api',
    version='1.0.0',
    description="A module to simplify Linode interactions.",
    long_description=open("README.md", "r").read(),
    author="Yunus Ruzmetov",
    author_email="waternewtinfo@gmail.com",
    url="https://github.com/WaterNewt/Linode-API",
    download_url="https://github.com/WaterNewt/Linode-API/releases/tag/v1.0.0",
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['requests'],
    python_requires='>=3.6',  # Specify the minimum Python version
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords=['Linode API interaction', 'API', 'cloud', 'Linode'],
    include_package_data=True,
)