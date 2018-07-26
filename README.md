# AZTK on ACI

Deploy scalable Spark clusters in seconds on top of Azure Container Instances


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

### CLI
Usage:
```bash
aztk-aci cluster create --id {id} --master-cpu 1 --master-memory-gb 2 --worker-cpu 2 --worker-memory-gb 4 --worker-count 5

aztk-aci cluster get --id {id}

aztk-aci cluster delete --id {id}
```

### SDK
See [sdk_example.py](./samples/sdk_example.py).

