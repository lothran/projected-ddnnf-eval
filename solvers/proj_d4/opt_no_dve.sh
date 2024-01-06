#!/bin/sh
cd "$(dirname "$0")"
set -e
LD_LIBRARY_PATH=. 
./d4 -m proj-counting   --partitioning-heuristic decomposition-static-proj-dual\
    --partitioning-heuristic-partitioner kahypar   \
    --partitioning-heuristic-simplification-equivalence true \
    --partitioning-heuristic-partitioner-np-cost 10 \
    --partitioning-heuristic-max-cut-ratio 0.6 \
    -i $1\
    --crs none \
    -p proj\
    --sm vsads2\
    --cache-alloc std\
    --cache-method lru-prob\
    --cache-fixed-size 12 \
    --preproc-equiv true \
    --preproc-ve-check true\
    --preproc-ve-only-simpical false\
    --preproc-ve-prefer-simpical true\
    --preproc-ve-limit 4 \
    --projddnnf-pure-lit-elim true \
    --scoring-method-decay-freq 128222222

