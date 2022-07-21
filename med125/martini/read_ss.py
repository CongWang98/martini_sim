import sys

file_name = sys.argv[1]
N = int(sys.argv[2])

ss_str = ''
#print(file_name)
with open(file_name, 'r') as f:
    line = f.readline()
    #print(line)
    while len(ss_str) !=N:
        if line[:3] == 'ASG':
            #print(line.split())
            ss_str += line.split()[5]
        line = f.readline()
print(ss_str) 
