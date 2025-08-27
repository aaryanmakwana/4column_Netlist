from numpy import genfromtxt
import numpy as np

netlist = genfromtxt('netlist.csv', delimiter=',',dtype="str")
output = np.zeros((netlist.shape[0]-1,3))

for i in range(netlist.shape[0]-1):
    output[i,0] = i+1
    output[i,1] = 1
    output[i,2] = 1

def simplify(net):
    if net[1]=="and":
        if output[int(net[0])-1,1]==1:
            output[int(net[2])-1,1] = 0
            output[int(net[3])-1,1] = 0

        simplify(netlist[int(net[2])])
        simplify(netlist[int(net[3])])

    elif net[1]=="nand":
        if output[int(net[0])-1,2]==1:
            output[int(net[2])-1,2] = 0
            output[int(net[3])-1,2] = 0

        simplify(netlist[int(net[2])])
        simplify(netlist[int(net[3])])

    elif net[1]=="or":
        if output[int(net[0])-1,1]==1:
            output[int(net[2])-1,2] = 0
            output[int(net[3])-1,2] = 0

        simplify(netlist[int(net[2])])
        simplify(netlist[int(net[3])])

    elif net[1]=="nor":
        if output[int(net[0])-1,1]==1:
            output[int(net[2])-1,2] = 0
            output[int(net[3])-1,2] = 0

        simplify(netlist[int(net[2])])
        simplify(netlist[int(net[3])])

    elif net[1]=="xor":
        simplify(netlist[int(net[2])])
        simplify(netlist[int(net[3])])

    elif net[1]=="xnor":
        simplify(netlist[int(net[2])])
        simplify(netlist[int(net[3])])

    elif net[1]=="not":
        if output[int(net[0])-1,1]==1 and output[int(net[0])-1,2]==1:
            type = netlist[int(net[2]),1]
            if type == "nor":
                output[int(net[2])-1,2] = 0
            elif type == "and":
                output[int(net[2])-1,2] = 0
            elif type == "nand":
                output[int(net[2])-1,1] = 0
            elif type == "or":
                output[int(net[2])-1,2] = 0

        elif output[int(net[0])-1,1]==0:
            output[int(net[2])-1,2] = 0
        else:
            output[int(net[2])-1,1] = 0

        simplify(netlist[int(net[2])])

    elif net[1]=="buff":
        output[int(net[2])-1,2] = 1
        output[int(net[2])-1,1] = 1

        simplify(netlist[int(net[2])])

    elif net[1]=="inpt":
        pass
    else:
        print("invalid")
        print(net)

n_out = 0

for net in netlist:
    if net[1]=="output":
        output[int(net[2])-1,2] = 1
        output[int(net[2])-1,1] = 1
        n_out += 1
        simplify(netlist[int(net[2])])

output = output[:(output.shape[0]-n_out),:]
print(output)
