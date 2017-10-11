from Scheduler import Scheduler
from numpy import ceil
import random 

V = {}
#f = open("SF.cnode.txt",'rU')
f = open("SF.small_nodes.txt",'rU')
for line in f:
    data = line.split(',')
    if data[0]!="":
        x = float(data[1])
        y = float(data[2])
        V[int(data[0])] = [x, y]
f.close()


E={}
f = open("SF.cedge.txt",'rU')
for line in f:
    data = line.split()
    if data[0]!="":
        if int(data[1]) in V and int(data[2]) in V:
            E[ ( min(int(data[1]) , int(data[2])) ,max(int(data[1]) , int(data[2]))   )]= ceil(float(data[3])/5) 
f.close()

random.seed(1)
Trucks={}
truckId = 0
for key in V:
    if random.random()<0.1:
        r = random.randint(15,40)
        for tmp in xrange(r):
            Trucks[truckId] = key 
            truckId=truckId+1
            
myScheduler = Scheduler(V, E, Trucks,True)

VList = V.keys()
orderId = 0
print "We have",truckId,"trucks,", len(VList), "nodes and ",len(E),'edges'


for orders in xrange(16):
    # create orders
    newOrders=[]
    for j in xrange(7):
        fromV = random.randint(0,len(VList)-1)
        toV = random.randint(0,len(VList)-1)
        while toV==fromV:
           toV = random.randint(0,len(VList)-1) 
        newOrders.append( (VList[fromV], VList[toV]) )
        
    myScheduler.processNewOrders(newOrders)

    for t in xrange(30):
        myScheduler.updateLocationOfTrucks()

for t in xrange(1200):
    myScheduler.updateLocationOfTrucks()

        
        
myScheduler.saveTravelHistoryOfAllTrucks()    
    
    
    
    
    
    



