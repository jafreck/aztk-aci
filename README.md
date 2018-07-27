# AZTK on ACI

Deploy scalable Spark clusters in seconds on top of Azure Container Instances (ACI)


## Overview

AZTK on ACI provisions Spark clusters in seconds.

Features:
- 20 second cluster deployment time
- heterogenous master and worker sizes


Limitations:
- Because of limitations to ACI, each node can have at most 4 cpus and 14 gb of memory. See [ACI Quota](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-quotas) for more details.
- ACI does not support VNETs yet, so all node communcation happens over public ip

Roadmap:
- Cluster resize support
- support for vnets, with single IP to submit application
- Job submission mode
- File upload


## Installation

### Install from pip
TBD

### Install from source

Clone the repo, create a virutal environment, and install the requirements

```sh
# create virutal environment, activate the environment
python -m venv env
source env/bin/activate # on Windows: env/Scripts/activate

# clone the repo
git clone https://github.com/jafreck/aztk-aci.git

# install the package
pip install -e aztk-aci/
```

## Usage

### Getting Started
TBD

### CLI
Usage:
```bash
aztk-aci cluster create --id {id} \
     --master-cpu 1 \
     --master-memory-gb 2 \
     --worker-cpu 2 \
     --worker-memory-gb 4 \
     --worker-count 5

aztk-aci cluster get --id {id}

aztk-aci cluster delete --id {id}
```

### SDK
See [sdk_example.py](./samples/sdk_example.py).

