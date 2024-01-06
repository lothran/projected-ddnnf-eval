#!/bin/bash
trap "exit" INT
output=$1
solver=$2
T=$3
for file in *.dimacs;
do
    file=$(realpath $file)
    id=$(basename $file)
    logfile=$output/$id
    echo "running: $solver $logfile"
    echo "launched">$logfile
    res="$( { time timeout $T bash $solver $file ; } 2>&1 )"
    if [ $? -eq 0 ]; then
        echo "success">>$logfile
    else
        echo "timeout">>$logfile
    fi
    echo "$res">>$logfile
done






