# -*- coding: utf-8 -*-
from mpi4py import MPI
import math
import random
from itertools import permutations

nb_sol = 50
generations = 100
mutation_rate = 5
nb_cls = 4

class Point:
    def __init__(self,x):
        self.data = x
        
    def distance(self,p):
        d = 0.
        for i in range(len(p.data)):
            delta = self.data[i]-p.data[i]
            d += delta*delta
        d = math.sqrt(d)
        return d

class Solution:
    def __init__(self,n):
        self.data = []
        self.sumdist = 0.
        self.nb_class = n

    def quality(self):
        self.sumdist = 0.
        for i in range(len(self.data)):
            for j in range(i+1,len(self.data)):
                if(self.data[i] == self.data[j]):
                    self.sumdist += points[i].distance(points[j])            
        return self.sumdist

    def random_solution(self,ncls,nb_points):
        self.data.clear()
        for i in range(nb_points):
            self.data.append(random.randint(0,ncls-1))

    def set_data(self,data):
        self.data = data

    def mutation(self,rate): 
        self.quality()
        val = self.sumdist
        for iter in range(rate):
            i = random.choice(range(len(self.data)))
            for k in range(self.nb_class):
                bck = self.data[i]
                self.data[i] = k
                self.quality()
                if(self.sumdist < val):
                    val = self.sumdist
                else:
                   self.data[i] = bck

    def crossover(self,data2,p):
        besti = 0 
        bestv = 0 
        for i in range(len(p)):  
            data = []
            val = 0
            for j in range(len(data2)):
                data.append(p[i][data2[j]])
            for j in range(len(data2)):
                if(self.data[j] == data[j]):
                    val += 1
            if(val > bestv):
                bestv=val
                besti=i
            data.clear()
        for j in range(len(data2)):
            if(random.choice([0,1]) == 0):
                self.data[j] = p[besti][data2[j]]
                
    def valid(self):
        for s in range(len(self.data)):
            if(self.data[s] > self.nb_class):
                print(s," data = ",self.data[s])
                return False
        return True
    def display(self):
        print(self.data)

class Population:
    def __init__(self):
        self.sols = []
        
    def addSolution(self,s):
        self.sols.append(s)
    
    def getData(self,i):
        if(i>= 0 and i<len(self.sols)):
            return self.sols[i].data
        else: 
            return None

    def setData(self,i,d):
        if(i>= 0 and i<len(self.sols)):
            self.sols[i].data = d
            
    def sort(self):
        for s in self.sols:
            s.quality()
        cont = True
        while cont:
            cont = False
            for i in range(len(self.sols)-1):
                if(self.sols[i].sumdist > self.sols[i+1].sumdist):
                    self.sols[i],self.sols[i+1] = self.sols[i+1],self.sols[i]
                    cont = True

    def randomGoodData(self):
        pos = random.randint(0,len(self.sols)//2)
        return self.sols[pos].data

    def randomData(self):
        c = len(self.sols)#//2
        pos = random.randint(0,c)#+c
        if(pos >= len(self.sols)):
            pos=0

        return self.sols[pos].data

    def replaceRandomBadData(self,d):
        c = len(self.sols)//2
        pos = random.randint(0,c)+c
        if(pos >= len(self.sols)): 
            pos=c
        self.sols[pos].data = d
        self.sols[pos].quality()
        
    def bestQuality(self):
        return self.sols[0].sumdist

    def bestData(self):
        return self.sols[0].data

    def valid(self):
        v = True
        for s in range(len(self.sols)):
            if(not self.sols[s].valid()):
                print(s," sol not valid")
                v = False
        return v

    def display(self):        
        for s in range(len(self.sols)):
            print(s," sol : ")
            self.sols[s].display()

perm_cls = list(permutations(list(range(nb_cls))))

points = []

inputfile = open("data.txt","r")
data = inputfile.readlines()

for line in data:
    p = []
    ltoken = line.split()
    for s in ltoken:
        p.append(float(s))
    points.append(Point(p))
nb_points = len(points)

tmp_sol = Solution(nb_cls)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


if(rank == 0):
    print("Nb Points = ",nb_points)
    population = Population()
    for i in range(nb_sol):
        s = Solution(nb_cls)
        s.random_solution(nb_cls,nb_points)
        s.quality()
        population.addSolution(s)
    population.sort()
    print("Initial solution value : ",population.bestQuality())
    for pid in range(1,size):
        data1 = population.randomGoodData()
        data2 = population.randomData()
        comm.send(data1,dest=pid)
        comm.send(data2,dest=pid)
        
for iter in range(generations):
    if(rank == 0):#master
        for pid in range(1,size):
            data = comm.recv()
            population.replaceRandomBadData(data)
            population.sort()
        for pid in range(1,size):        
            data1 = population.randomGoodData()
            data2 = population.randomData()
            comm.send(data1,dest=pid)
            comm.send(data2,dest=pid)
        print("It ",iter+1," solution value : ",population.bestQuality())
    else:#slave
        data1 = comm.recv(source=0)
        tmp_sol.set_data(data1)
        data2 = comm.recv(source=0)
        tmp_sol.crossover(data2,perm_cls)
        tmp_sol.mutation(mutation_rate)
        comm.send(tmp_sol.data,dest=0)

#finalisation
if(rank == 0):
    for pid in range(1,size):
        data = comm.recv()
        population.replaceRandomBadData(data)
        population.sort()
    print("Final solution value : ",population.bestQuality())
    print("Final solution : ",population.bestData())
else:
    data1 = comm.recv(source=0)
    tmp_sol.set_data(data1)
    data2 = comm.recv(source=0)
    tmp_sol.crossover(data2,perm_cls)
    tmp_sol.mutation(mutation_rate)
    comm.send(tmp_sol.data,dest=0)
