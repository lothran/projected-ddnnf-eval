#!/bin/bash

# $1, path to the bench
# $2, problem type (mc, wmc or pmc)


cd "$(dirname "$0")"
echo "c [COMMAND LINE]: $@"

CURR_PATH="."
OPTIONS="-p sharp-equiv"

BENCH=$1
TYPE=pmc


$CURR_PATH/d4_static -m counting -i $BENCH --keyword-output-format-solution "s type $TYPE" --output-format competition $OPTIONS
