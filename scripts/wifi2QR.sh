#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "/opt/apps/WifiQRGenerator/scripts/config.cfg"

bash -c "${PYTHON_INTERPETER} ${HOME_FOLDER}/src/wifi2QR.py $@"
