#!/bin/bash
PWD=$(pwd)
export PYTHONPATH="${PYTHONPATH}:${PWD}"
cd src/Server/
python3 server.py