# Page Status

## Setup the Page Status tool
To run the `Page Status` tool, `Python` needs to be installed. Begin be checking that `Python` is installed on your machine:

```shell
$ python3 --version
```

The repository can be cloned using `Git`. `SSH` has been setup:

```shell
$ git clone git@github.com:hackdanismo/automation.git
```

Once cloned, change directory to the subfolder containing the `page-status` code and install the dependencies:

```shell
# Change directory into the main project folder
$ cd automation
# Change directory into the subfolder containing the page-status tool
$ cd page-status

# Setup the Virtual Environment to create the venv folder
$ python3 -m venv venv
# Activate the Virtual Environment
$ source venv/bin/activate

# Install the dependencies listed in the requirements.txt file
$ pip3 install -r requirements.txt
```

## Run the Page Status tool
Once setup has been completed, the following process can be used to run the tool:

```shell
# Change directory into the main project folder
$ cd automation
# Change directory into the subfolder containing the page-status tool
$ cd page-status

# Activate the Virtual Environment
$ source venv/bin/activate

# Run the Python script containing the code for the tool locally
$ python3 index.py

# To close the tool and end the Virtual Environment session
$ deactivate
```

The script will run once per day, using `GitHub Actions`, at: `00:00 UTC`.