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

for file in glob.glob(f"{input}/**/*.dimacs",recursive=True):
    segments = file.split("/");
    solver = segments[-3]
    if solver not in solver_results:
        solver_results[solver] = []
    instance = segments[-2]+segments[-1]
    with open(file,"r") as f:
        result = f.read()
        split_match = re.search(r"c Number of split formula: ([0-9]*)",result)
        dec_match = re.search(r"c Number of decision: ([0-9]*)",result)
        
         
        if( split_match==None or dec_match==None):
            print("missing match "+instance)
            continue
        number_of_nodes = int(split_match.group(1))+int(dec_match.group(1));
        if number_of_nodes <2:
            print("sus "+ instance)
        solver_results[solver].append(number_of_nodes)

for name,results in solver_results.items(): 
     results.sort()
     with open(output+"/"+name+".csv","w") as outfile:
        writer = csv.writer(outfile,delimiter=",")
        writer.writerow(["id","time"])
        for i,r in enumerate(results):
            writer.writerow([i,r])



    


    

    
    





