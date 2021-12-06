#!/bin/sh

black --check .
isort --check .
flake8 .
