#! /bin/bash

./venv/bin/pip install coverage pytest
./venv/bin/coverage run --source=./robinwould -m pytest
clear

./venv/bin/coverage report