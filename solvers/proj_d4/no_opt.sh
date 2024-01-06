#!/bin/sh
cd "$(dirname "$0")"
set -e
LD_LIBRARY_PATH=. ./d4 -m proj-ddnnf-compiler\
    --partitioning-heuristic none \
    -i $1 \
    --proj-backup none 
