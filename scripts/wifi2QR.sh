#!/usr/bin/env bash

source /opt/venv/bin/activate
python3 /opt/venv/apps/WifiQRGenerator/src/wifi2QR.py $@
deactivate