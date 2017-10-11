from scipy.spatial import distance
# from Scheduler import Scheduler
from coinor.blimpy import Stack, Queue





class Truck:

    

    

    def __init__(self, _id, initialLocation):
        self.id = _id
        self.history = []
        self.currentLocation = [initialLocation, None, None, None,None] #(start, destination, minute in, total time) 
        self.myTasks = Queue()
        
    """

    adding tasks to myTask: (pickupLoc, deliveryLoc) 

    """    

    def addOrder(self, taskList,type):
        #list of tasks are input and added to list
        for task in taskList:
            self.myTasks.enqueue(task)
         #this type will be set equal to none if truck already ready to pickup
        if type!=None:
            self.currentLocation = self.myTasks.dequeue()
        

        #self.currentLocation = [self.initialLocation, pickUpLocation, 0, self.get_edge_attr(self.initialLocation, pickUpLocation, distance)] 

        #self.myTasks.push(self.currentLocation)
    """

    Current location of a truck should be either at Node or on a "directed" edge

    together with the information how far on this edge the truck is.

    """    

    def updateLocation(self):
        # if no tasks and doing nothing, keep the same
        if self.myTasks.isEmpty() and self.currentLocation[1]==None: 
            self.currentLocation = [self.currentLocation[0], None, None, None]
        #otherwise, update location
        else: 
            self.currentLocation[2] = self.currentLocation[2]+ 1 #update the location very minute 
            #if destination is reached, adjust current location and add to history
            if self.currentLocation[2] == self.currentLocation[3]:
                self.history.append(self.currentLocation)
                #if done, stop, else continue to next task
                if self.myTasks.isEmpty():
                    self.currentLocation = [self.currentLocation[1], None, None, None]
                else: 
                    self.currentLocation = self.myTasks.dequeue()


              
    def isIdle(self):
        #check if truck has tasks
        return self.myTasks.isEmpty()
    """

         it should return the edge and also how far he is on this edge, e.g. [A,C],[5,30] 

         if he is traveling 5 minutes on an edge A->C which takes 30 minutes to travel 

    """

    def getCurrentLocation(self): 
        return self.currentLocation

    
    """

    This should return total travel history, e.g.

    A,C,30/30,P20;P94;P101    # this means he moved from A to C which was 30 minutes out of 30 minutes, he picked up 3 packages

    C,D,30/40    # then he was traveling from C to D, only for 30 minutes (so he did not get to D)

    D,C,30/40,P33;P34    # then he turn around and went back to C for 30 minutes and picked up 2 packages

    C,E,50/50,D33;D20    # then he went to E and drop package 33 and 20

    """

    def getTotalTravelHistory(self):
        self.history.append(self.currentLocation)
        return self.history