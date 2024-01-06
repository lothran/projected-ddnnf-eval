import sys
import glob
import os
import re
import csv


def parse_time(arg:str):
    segs = arg.split('m')
    sec=segs[1].replace("s","")
    min=segs[0]
    return float(sec)+float(min)*60;



input = sys.argv[1]
output = sys.argv[2]
max_time = float(sys.argv[3])
solver_results = {}
acc_time = {}
counter = {}


for file in glob.glob(f"{input}/**/*.dimacs",recursive=True):
    segments = file.split("/");
    solver = segments[-3]
    instance = segments[-2]+segments[-1]
    base_instance = segments[-2]

    if solver not in solver_results:
        solver_results[solver] = {}
    if base_instance not in solver_results[solver]:
        solver_results[solver][base_instance] = []
    if base_instance not in acc_time:
        acc_time[base_instance] = 0
        counter[base_instance] = 0

    with open(file,"r") as f:
        result = f.read()
        time_match = re.search(r"real\s*([^\n]*)\nuser\s*([^\n]*)\nsys\s*([^\n]*)\n",result)
        split_match = re.search(r"c Number of split formula: ([0-9]*)",result)
        result_mc2022 = re.search(r"c s exact arb int [0-9]*",result)
        result_d4 = re.search(r"\ns [0-9]*",result)
        
        if(time_match==None or (result_d4 == None and result_mc2022==None )):


            print(solver," failed ",instance)

            continue

        real_time = parse_time(time_match.group(1));
        cpu_time = parse_time(time_match.group(2));
        sys_time = parse_time(time_match.group(3));
        time = real_time;
        if real_time<max_time:
            solver_results[solver][base_instance].append(real_time)
        else:
            print(solver," failed ",instance)

        acc_time[base_instance] += real_time
        counter[base_instance] +=1



print(counter)
avg_time = [ (acc[0],acc[1]/(counter[acc[0]]+1)) for acc in acc_time.items()]


avg_time =  list(reversed(sorted(avg_time,key=lambda x:x[1])))

print(avg_time)


with open(output,"w") as outfile:
    writer = csv.writer(outfile,delimiter=",")
    header = ["id"]
    for k,v in solver_results.items():
        header.append(k)
    writer.writerow(header)
    for  i in avg_time[:10]:
        line = [i[0]]
        for k,v in solver_results.items():
            line.append(len(v[i[0]]))
        writer.writerow(line)






    


    

    
    





