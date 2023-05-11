# Remote controlled car

TODO: Add description about project and specifications.

## Setup

### OS package dependencies

Assuming Ubuntu 18.04, to install required OS packages, run:

```
scripts/install_packages.sh
```

### virtualenv

The project is designed to run in a Python 3.6+ virtual environment. To set up the venv, run:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Maestro config

There is a configuration for the Maestro controller in `configs/maestro.xml`. This config should be
applied to the controller before running.

## Running

To enter the virtual environment, run:

```
source venv/bin/activate
```

Then, to run the main script, run:

```
python3 __main__.py
```
