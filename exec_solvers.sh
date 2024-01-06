#!/bin/bash
SOLVERS=/solvers
MODELS=$1
RESULTS=$2
QUEUE=$3
MEM=$4
INSTANCE_TIME=$5
TOTAL_TIME=$6
N=$7
declare -A solvers
#solver table make sure these match with scripts inside the login node
solvers[gpmc]=gpmc/default.sh
solvers[proj_d4]=proj_d4/opt_no_dve.sh
solvers[slice]=proj_d4/slice.sh
solvers[d4_pmc]=d4/d4/bin/starexec_run_default.sh
solvers[arjun]=sharpsat-td-arjun/starexec_run_track3_conf2.sh
for file in $MODELS/**/*.dimacs;
do
    id=$(basename $file)
    dir=$(dirname $file)
    prefix=$(basename $dir)
    for solver_name in "${!solvers[@]}";do
        mkdir -p $RESULTS/$solver_name/$prefix
    done

done
for dir in $MODELS/*;
do
    prefix=$(basename $dir)
    for solver_name in "${!solvers[@]}";do
        output=$RESULTS/$solver_name/$prefix
        echo running $output
        sbatch -W -p $QUEUE --container-name=archlinux:no_exec\
            --container-workdir=/input \
            --container-mounts=/etc/slurm/task_prolog:/etc/slurm/task_prolog,/scratch:/scratch,$dir:/input,$output:/output\
            -n 1 -t $TOTAL_TIME --mem=$MEM\
            exec_array.sh /output $SOLVERS/${solvers[$solver_name]} $INSTANCE_TIME &
        echo started $output
        if [[ $(jobs -r -p | wc -l) -ge $N ]]; then
            # now there are $N jobs already running, so wait here for any job
            # to be finished so there is a place to start next one.
            #
            echo waiting for slot
            wait -n
        fi

    done
done
wait

