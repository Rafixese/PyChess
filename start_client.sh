#!/bin/bash
PWD=$(pwd)
export PYTHONPATH="${PYTHONPATH}:${PWD}"
cd src/Client/
python3 login.py