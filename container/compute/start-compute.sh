#!/usr/bin/bash

set -x

export PYTHONPATH=.

#export KUBECTL="$PWD/remote-kubectl"
#export CURL="$PWD/remote-curl"

python3 -b -B -m compute

