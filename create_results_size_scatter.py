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
instance_results = {}


solvers = []
for file in glob.glob(f"{input}/**/*.dimacs",recursive=True):
    segments = file.split("/");
    solver = segments[-3]
    instance = segments[-2]+segments[-1]
    if instance not in instance_results:
        instance_results[instance] = {}
    if solver not in solvers:
        solvers.append(solver)
    with open(file,"r") as f:
        result = f.read()
        split_match = re.search(r"c Number of split formula: ([0-9]*)",result)
        dec_match = re.search(r"c Number of decision: ([0-9]*)",result)
        cnt_match = re.search(r"\ns ([0-9]*)",result)
     
        if( split_match==None or dec_match==None or cnt_match == None):
            continue
        number_of_nodes = int(split_match.group(1))+int(dec_match.group(1));
        instance_results[instance][solver]  = (number_of_nodes,cnt_match.group(1))

solvers = sorted(solvers)
print(solvers)
assert(len(solvers)==2)
results = []
for i,e in instance_results.items():
    if len(e) != 2:
        continue
    val = list(e.items())[0][1][1]
    ok = True
    for s,v in list(e.items()):
        if v[1] != val:
            ok = False
        if v[0] == 0:
            ok = False
        e[s] = v[0]
    if not ok:
        print("no ok ",i)
    values = [i]
    for s,v in sorted( e.items(),key=lambda x:x[0]):
        if v==0:
            v=1
        values.append(v)
    results.append(values)
results = sorted(results,key=lambda x:x[0])
print(yaml.dump(results))
a = 0
b = 0
smaller=0
bigger=0
acc_avg = 0
avg_cnt = 0
total_cnt =  0
with open(output,"w") as outfile:
    writer = csv.writer(outfile,delimiter=",")
    writer.writerow(solvers)
    for w,i,r in results:
        writer.writerow([i,r])
        if i>10000 and r>10000 or True:

            if i<r:
                smaller+=1
            else :
                bigger+=1
            a+=i
            b+=r
            total_cnt +=1
            acc_avg += r/i
            avg_cnt+=1
print("smaller: ", smaller)
print("bigger: ", bigger)
print("avg: ",acc_avg/avg_cnt)
print("a/b: ", a/b)
print("b/b: ", b/a)
print("a/tct: ", a/total_cnt)

print("b/tct: ", b/total_cnt)




    


    

    
    





