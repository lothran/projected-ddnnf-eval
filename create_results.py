import sys
import glob
import os
import re
import csv
import yaml


def parse_time(arg:str):
    segs = arg.split('m')
    sec=segs[1].replace("s","")
    min=segs[0]
    return float(sec)+float(min)*60;



input = sys.argv[1]
output = sys.argv[2]
max_time = float(sys.argv[3])
solver_results = {}

inst_info = {}

for file in glob.glob(f"{input}/**/*.dimacs",recursive=True):
    segments = file.split("/");
    solver = segments[-3]
    if solver not in solver_results:
        solver_results[solver] = []
    instance = segments[-2]+segments[-1]

    if instance not in inst_info:
        inst_info[instance] = {};
    if solver not in inst_info[instance]:
        inst_info[instance][solver] = []
    with open(file,"r") as f:
        result = f.read()
        time_match = re.search(r"real\s*([^\n]*)\nuser\s*([^\n]*)\nsys\s*([^\n]*)\n",result)
        split_match = re.search(r"c Number of split formula: ([0-9]*)",result)
        result_mc2022 = re.search(r"c s exact arb int ([0-9]*)",result)
        result_d4 = re.search(r"\ns ([0-9]*)\n",result)

        if(time_match==None or (result_d4 == None and result_mc2022==None )):
            continue
        real_time = parse_time(time_match.group(1));
        cpu_time = parse_time(time_match.group(2));
        sys_time = parse_time(time_match.group(3));
        time = real_time;
    
        result = result_d4 or result_mc2022
        result = int(result.group(1))
        if real_time<max_time:
            inst_info[instance][solver].append((real_time,result))
        else:
            print(solver," failed ",instance)
for instance_name,solver_resuls in inst_info.items():
    val = None
    for solver,results in solver_resuls.items():
        real_time = 0.0;
        cnt= 0;
        for result in results:
            real_time+=result[0]
            cnt += 1
            if val == None:
                val = result[1]
            elif val != result[1]:
                print(f"bad results for {solver} on {instance_name}: {val} vs {result[1]}")
        if(cnt>0):
            solver_results[solver].append(real_time/cnt)   
for name,results in solver_results.items(): 
     results.sort()
     with open(output+"/"+name+".csv","w") as outfile:
        writer = csv.writer(outfile,delimiter=",")
        writer.writerow(["id","time"])
        for i,r in enumerate(results):
            writer.writerow([i,r])
print(yaml.dump(inst_info))



    


    

    
    





