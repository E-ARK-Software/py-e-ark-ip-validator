E-ARK Python IP Validator
=========================

Core package and command line utility for E-ARK Information Package validation.

Quick Start
-----------
### Pre-requisites
Python 3.5+ 

### Getting the code
Clone the project move into the directory:

```shell
git clone https://github.com/E-ARK-Software/py-ip-validator.git
cd py-ip-validator
```

### Installation

#### Local virtual env setup
Set up a local virtual environment:

```shell
virtualenv -p python3 venv
source venv/bin/activate
```

Install the requirements:

```shell
pip install -r requirements.txt
```

### Run

From the command line do:

```shell
python py_ip_validator/validator.py -i <path_to_directory_or_package>
```

If `input` is a directory, it must contain a single folder which contains the information package (and no other files or folders):

```shell
user@machine:~$ tree input
input
└── my_package
    ├── documentation
    ├── metadata
    ├── METS.xml
    ├── representations
    │   └── rep1
    │       ├── data
    │       ├── metadata
    │       └── METS.xml
    └── schemas
```

### Running tests

You can run unit tests by:

    pytest ./tests/

and generate test coverage figures by:

    pytest --cov=ip_validation ./tests/

If you want to see which parts of your code aren't tested then:

     pytest --cov=ip_validation --cov-report=html ./tests/

After this you can open the file [`<projectRoot>/htmlcov/index.html`](./htmlcov/index.html) in your browser and survey the gory details.
