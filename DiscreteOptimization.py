#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import pandas as pd
import numpy as np
from tabulate import tabulate
import itertools
from operator import itemgetter
import cython
#may try out cython to improve the run time via c code


#namedtuple is a class obejct that creates immutable objects; tuples
Item = namedtuple("Item", ['index', 'value', 'weight'])


class discreteOptimization(object):
    """No need for initilization because we are taking data from an outside source and not creating new data"""
    
    def theoreticalMaximum(items, tempcapacity): 
        """a copy of items and capactiy are brought in if no other variables are specified
        theoreticalMaxiumum is the maximum if you consider partial items this helps with the 
        greedy tree based calculations """
        
        items = filter(lambda x: (x[2] < tempcapacity), items)
        #filter that removes any items that weight more than the capacity
        itemsort = sorted(items, key=lambda y: float(y[2])/float(y[1]))
        #sort items by their price over weight
        tempvalue=0
        tempwvalue = 0
        for item in itemsort:
            if item.weight < tempcapacity:
                tempcapacity -= item.weight
                tempvalue += item.value
            elif tempcapacity != 0:
                tempvalue += float(item.value)/float(item.weight)*float(tempcapacity) #numerator and denominator are required to be floats to properly calculate
                tempcapacity = 0
        return tempvalue
    
class dynamicProgramming(discreteOptimization):    
    """This class holdes the dynamic programming methods"""
    
    def optimal(k, j,item,items):
        #recursive method called to calculate the the table in dynamic programming
        if (j<0):
            return 0
        elif (item[2]<=k):            
            return max(dynamicProgramming.optimal(k,j-1,items[j-1], items),(item[1]+dynamicProgramming.optimal(k-item[2],j-1,items[j-1],items)))
        else:
            return dynamicProgramming.optimal(k,j-1, items[j-1],items)
        
        
    def dynamic(taken, value, capacity, lasttaken,items):
    ##For Dynamic Programming Fill's out array with optimal values
        a= np.zeros(len(items))
        for j in range(0,len(items)):
            a[j] =  dynamicProgramming.optimal(capacity, j, items[j], items)
        lt2 = lasttaken
        ##starts from the end, Once the last is found recalculate the array
        for g in range(lt2-1,0,-1):
            if a[g] != a[g-1]:
                if items[g].weight <= capacity:
                    lasttaken = g        
                    taken[lasttaken]=1
                    value += items[lasttaken].value
                    capacity -= items[lasttaken].weight
                    return dynamicProgramming.dynamic(taken,value,capacity,lasttaken, items)
    
        return lasttaken, value, capacity, taken
    

def solve_it(input_data):
    # Modify this code to run the optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    
    print(items)
    
    value = 0
    weight = 0
    taken = [0]*len(items)
    hvalue = 0
    hweight = 0 
    htaken = [0]*len(items)
    lasttaken = len(items)

    lasttaken, value, capacity,taken = dynamicProgramming.dynamic(taken, value, capacity, lasttaken, items) 
    #calls the descreteOptimization class and uses the dynamic method
 
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

    
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 0:
        file_location = sys.argv[0].strip()
        with open("./data/ks_30_0", 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

