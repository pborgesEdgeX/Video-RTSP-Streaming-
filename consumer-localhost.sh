#!/bin/bash
source `which virtualenvwrapper.sh`
mkvirtualenv --python=`which python3` consumer_local
workon consumer_local
cd ./consumer_localhost/
pip install -r requirements.txt
python3 main.py