#!/bin/bash

cd "$(dirname "$0")"
./gpmc -mode=2 $1
