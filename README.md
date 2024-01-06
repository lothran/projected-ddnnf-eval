# projected d-dnnf eval 
## How To Run
These scripts are intended to be run on the BW-Uni-Cluster and use slurm and enroot.
For more info on the cluster read [this](https://wiki.bwhpc.de/e/BwUniCluster2.0).
The setup was done badly and was never intended for easy replication.
To get started follow these steps:
- git this repository into the login node
- use enroot to create an archlinux container named archlinux
- build open-source solvers (D4 and gpmc) from inside the container
- copy binaries for none open-source solver inside the container
- also copy run scripts for solvers into the container
- inside the container put solver and solver run scripts in `/solvers/<solver_name>/<solver_exe><solver_runscript.sh>`
- inside exec_solver.sh make sure the solver table matches the solver run scripts inside `/solvers/<solver_name>` inside the container 
- look at the solvers directory inside this repository for examples used in the thesis (you should rebuild the binaries for d4 because they are stale)
- each solver run script will be called with the path to a dimacs instance
- all solver specific arguments should be set inside the solver run script
- each solver will be run in parallel
- inside the login node package dimacs instances into the following structure:
    `<experiment>/<chunk>/<0.dimacs>...`
- each chunk will run in parallel 
- instances inside chunks will be run serially
- place packaged instances somewhere in the login node
- launch one master job that will dynamically create more jobs when slots are available
- launch with `sbatch --mem=1000 -t TIME_LIMIT -p QUEUE -n 1 exec_solver.sh MODELS RESULTS QUEUE MEM INSTANCE_TIME TOTAL_TIME N`
- MODEL=path to instances, RESULTS=where to put results, QUEUE=[slurm-queue](https://wiki.bwhpc.de/e/BwUniCluster2.0/Batch_Queues), MEM=Memory per Chunk,
    INSTANCE_TIME=time per dimacs instance TOTAL_TIME=time per chunk N=number of parallel jobs(limited to ~50 for students)
- if everything works you should get results as solver logs inside the RESULTS directory
- start as many replicate master jobs as you like with new RESULTS directories for more accuracy (beware of job user limits...)
- make sure to put all results from different runs inside one common directory like this `ALL_RESULTS/<RESULTS1>,<RESULTS2>...`
- you can also modify stuff to exclude or rerun certain solver, old logs will be overwritten
- now you can extract data from solver logs with the python scripts
- `create_results.py ALL_RESULTS OUTPUT_CSV 3600` creates average cactus runtime tables for 
    each solver as csv files with a timeout of 3600 seconds. The csv's will be put inside the OUTPUT_CSV folder. 
    It averages all runtimes from different jobs inside the ALL_RESULTS folder.
- create_results_table.py will produce a table with the number of solved instances inside a chunk for each solver
- create_results_scatter.py creates a scatter plot of the d-dnnf sizes of exactly two solvers 
- create_results_table.py and create_results_scatter.py should only be used on a single RESULTS folder since they don't combine different jobs  
## Instances
Download:  
https://mega.nz/file/GahCkIJJ#3tGeuYTeU3x16Otn_KwNjoxE6SuL43UGbB1_ilKC5nM  
The data directory contains instances used in the thesis.
You can also generate more instances inside the generate directory.  
`python generated.py base_models/all.csv 50 0.2 0.9`
## Known Problems
- When chunks are out of memory they are stopped by slurm without considering other instances inside the chunk. 
Hence, all the MC2022 instance are run in their own chunk. For generated instances which are all run inside one chunk
this can be a problem when runtime is longer than 10min and 16GB ram is available.
- Creating to many concurrent master jobs will hit the user limit inside the cluster.
Managing the job limit with multiple master jobs is tricky, 
there should be single jobs which runs each instance for a specified amount of times.



