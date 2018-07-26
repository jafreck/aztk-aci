import fnmatch
import os

from setuptools import find_packages, setup

from aztk_aci import version
from aztk_aci_cli import constants

data_files = []


def _includeFile(filename: str, exclude: [str]) -> bool:
    for pattern in exclude:
        if fnmatch.fnmatch(filename, pattern):
            return False

    return True


def find_package_files(root, directory, dest=""):
    paths = []
    for (path, _, filenames) in os.walk(os.path.join(root, directory)):
        for filename in filenames:
            if _includeFile(filename, exclude=["*.pyc*"]):
                paths.append(os.path.relpath(os.path.join(dest, path, filename), root))
    return paths


with open('README.md', encoding='UTF-8') as fd:
    long_description = fd.read()

setup(
    name='aztk_aci',
    version=version.__version__,
    description='Deploy scalable Spark clusters in seconds on top of Azure Container Instances',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jafreck/aztk-aci',
    author='Microsoft',
    author_email='jafreck@microsoft.com',
    license='MIT',
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "azure-mgmt-containerinstance~=1.0.0",
        "pylint~=1.9.1",
        "pyyaml~=3.12",
        "yapf~=0.22.0",
        "msrestazure~=0.4.31",
        "azure-mgmt-resource~=1.2.2",
        "azure-storage-blob~=1.1.0",
        "azure-cosmosdb-table~=1.0.4",
        "azure-mgmt-storage==1.5.0",
    ],
    package_data={
        'aztk_aci': find_package_files("aztk", ""),
        'aztk_aci_cli': find_package_files("aztk_cli", ""),
    },
    scripts=[],
    entry_points=dict(console_scripts=["{0} = aztk_aci_cli.entrypoint:main".format(constants.CLI_EXE)]),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={
        'Documentation': 'https://github.com/Azure/aztk/wiki/',
        'Source': 'https://github.com/Azure/aztk/',
        'Tracker': 'https://github.com/Azure/aztk/issues',
    },
    python_requires='>=3.5',
)
