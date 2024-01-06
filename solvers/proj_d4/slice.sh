#!/bin/sh
#
cd "$(dirname "$0")"
set -e
sliced=$(mktemp)
java -Xss512m -jar my_slice.jar $1 ${sliced}
LD_LIBRARY_PATH=. ./d4 -m counting  -i ${sliced}

