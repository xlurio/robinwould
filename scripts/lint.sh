#! /bin/bash

./venv/bin/pip install pylint
clear

./venv/bin/pylint --disable=R0903 --disable=W0102 ./robinwould ./tests