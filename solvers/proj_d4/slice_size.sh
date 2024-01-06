#!/bin/sh
#
cd "$(dirname "$0")"
set -e
sliced=$(mktemp)
ddnnf=$(mktemp)
java -jar my_slice.jar $1 ${sliced}
LD_LIBRARY_PATH=. ./d4 -m ddnnf-compiler  -i ${sliced} --dump-ddnnf ${ddnnf} &> /dev/null
du -S ${ddnnf} | grep -o '^[0-9]*' 

