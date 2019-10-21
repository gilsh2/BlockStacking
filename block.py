# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:55:53 2019

@author: Alon Lapid
"""

import sys
import re

def custom_compare(a, b):
    return a.x * a.y  - b.x * b.y

def base(a):
    return a.x * a.y

#Class the hold the box demintions
class Block:   
    def __init__(self, x, y, z):     
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "(" + str(self.x) +"," +str(self.y) +"," +str(self.z) +")" 
    
    def __eq__(self, other): 
        if(self.x == other.x and  self.y == other.y and self.z == other.z)  : 
            return True
        else: 
            return False

def GetSolution(optimalHeightArray,optimal,stacking):
    solution = [] 
    startblock = optimalHeightArray.index(optimal);
    next = startblock
    while (True):                         
        solution.append(Blocks[next -1])
        next = stacking[next]
        if(next == 0 or next == None):
            break
    solution.reverse()    
    return  solution
       

#Initialization 
inputfile = ""
outputfile =""
if(len(sys.argv) > 2):
    inputfile = sys.argv [1]
    outputfile = sys.argv [2]
else :
    inputfile = "in.txt"
    outputfile = "out.txt"

# Reading input data     
inh = open(inputfile)
numberoflines = int(inh.readline());
Blocks = [] 
for i in range(1,numberoflines+1):
    line = inh.readline().strip();
    line = line.replace(",","").replace("{","").replace("}","")
    l = list(map(int, re.split('\s+', line)))    
    x = l[0]
    y= l[1]
    z = l[2]     
    #Insert all 3 rotation of the box type
    Blocks.append( Block(min(x,y),max(x,y),z))
    Blocks.append(Block(min(z,x),max(z,x),y))
    Blocks.append(Block(min(z,y),max(z,y),x))

# Sorting boxes according to base area     
Blocks = sorted(Blocks, key=base, reverse=True )    
    

optHeightArray  = [None] * (len(Blocks)+1)
optHeightArray[0] =0
stacking  = [None] * (len(Blocks)+1)

# Computing all the solutions from i to n in which the ith block is ontop using the recursion nature of the problem
# The i+1 solution evalutes all 1..i previous solution(stack of blocks) and find the best one to utilize ( or non at all) to place the i+1
#box ontop of it.
for i in range(1,len(Blocks)+1):
    maxHeightIndex = 0
    for j in reversed(range(0,i) ):        
        if(Blocks[j].x > Blocks[i-1].x and  Blocks[j].y > Blocks[i-1].y   ):
            if(optHeightArray[maxHeightIndex] < optHeightArray[j+1]):
                        maxHeightIndex = j+1                          
                        #print("set maxHeightIndex as  " + str(Blocks[j]) + ">" + str(Blocks[i-1])  ,i,j)                
                        
    # Adding block i on top of the best stack found from previous solutions              
    optHeightArray[i]=optHeightArray[maxHeightIndex] + Blocks[i-1].z;    
    stacking[i] = maxHeightIndex;


# getting the maximum stack out of all the stacks we computed 
optimalHeight = max(optHeightArray);


# Get the solution
solution = GetSolution(optHeightArray,optimalHeight,stacking)
print("The tallest tower has " + str(len(solution)) + " blocks and a height of " +str(optimalHeight))

#write the output
outh = open(outputfile, "w")
outh.write(str(len(solution)) + "\n" ) 
for block in solution:
    s = str(block.x)  + " " +  str(block.y) + " " + str(block.z) 
    if(len(sys.argv) < 2):
        print(s)
    outh.write(s+"\n" )     
    
outh.flush()
outh.close()  
    