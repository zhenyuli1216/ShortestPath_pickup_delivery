from Truck import Truck
from coinor.gimpy import Graph, DIRECTED_GRAPH
import pygame
import random
#import StringIO

class Scheduler:
    
    
    """
    V - set of vertices, key=ID, value=coordinates
    E - edges (hashtable), key=edge, value="length" in minutes
    Trucks - key=ID, value=Initial Location of a truck
    """
    def __init__(self, V, E, Trucks, makeAnimation):
        self.myTrucks=[]
        #create order num that will increase with each order
        self.orderNum = 1
        self.network = Graph(type = DIRECTED_GRAPH)
        pygame.init()
        self.img = pygame.image.load('takac.png')
        self.screenDimension = (940, 780)
        self.screen = pygame.display.set_mode(self.screenDimension)
        self.screen.fill((244, 238, 224))
        w1,h1 = self.img.get_size()
        self.img = pygame.transform.scale(self.img, (int(w1*0.07), int(h1*0.07)))
        self.framerate = 8
        
        
        self.edgeList = E
        #self.display.set_caption("Awesome team")
        #background = self.screen.convert()
        self.clock = pygame.time.Clock()
        self.coordinates = {} #a coordinate hashtable for scaled coordinate  
        maxX = 0
        maxY = 0
        minX = 'inf'
        minY = 'inf'
        for node in V: 
            if V[node][0] <= minX: 
                minX = V[node][0]
            if V[node][1] <= minY: 
                minY = V[node][1]
            if V[node][0] >= maxX: 
                maxX = V[node][0]
            if V[node][1] >= maxY: 
                maxY = V[node][1]
        self.factor = ((self.screenDimension[0]-55)/(maxX-minX), (self.screenDimension[1]-55)/(maxY-minY))
        for node in V: 
            self.network.add_node(node)
            self.coordinates[node] = (((int((V[node][0]-minX)*self.factor[0])),(int((V[node][1]-minY)*self.factor[1]))))
        #print coordinates
         
        for edge in E: 
            self.network.add_edge(edge[0],edge[1],cost=E[edge])
            pygame.draw.line(self.screen, (139, 69, 19), self.coordinates[edge[0]], self.coordinates[edge[1]], 2)
            self.network.add_edge(edge[1],edge[0],cost=E[edge])
               
        for node in self.coordinates: 
            #self.screen.blit(self.house, self.coordinates[node])
            pygame.draw.circle(self.screen, 
                               (random.randint(100, 255), random.randint(200, 255), random.randint(50, 255)), 
                                 self.coordinates[node] , 10, 0)    
#             
        
            
        #framrate = 10   
        pygame.display.update() 
        #clock.tick(200000)
        
#         self.network.set_display_mode('pygame')
#         self.network.display()    
#        self.display()
            
        for k in Trucks:
            self.myTrucks.append( Truck(k, Trucks[k])  )   
            
        validity, self.distance, self.nextn = self.network.floyd_warshall()
        

    """
        use shortest path method to find trucks to pickup packages and
        consequentially deliver them
    """
    def processNewOrders(self, newOrders):
        startTruck=[]
        for truck in self.myTrucks :
            startTruck.append(truck.currentLocation[0])  
        for order in newOrders:
            startPoint = order[0]
            endPoint = order[1]
            if startPoint in startTruck:
                if self.myTrucks[startTruck.index(startPoint)].isIdle():
                    chosen = startTruck.index(startPoint)
                    Scheduler.createOrder(self,self.myTrucks[chosen],startPoint, endPoint,1,'D'+str(self.orderNum))
                    self.orderNum = self.orderNum+1
            else:
                minD = 'inf'
                for position in startTruck:
                    i=startTruck.index(position)
                    if self.myTrucks[i].isIdle() and self.distance[(position,startPoint)]<=minD:
                        minD = self.distance[(position,startPoint)]
                        choose = position
                chosen = startTruck.index(choose)      
                Scheduler.createOrder(self, self.myTrucks[chosen],self.myTrucks[chosen].currentLocation[0], startPoint,1,'P'+str(self.orderNum))
                Scheduler.createOrder(self, self.myTrucks[chosen],startPoint, endPoint,None,'D'+str(self.orderNum))
                self.orderNum = self.orderNum + 1
            pygame.draw.circle(self.screen,(13,200,15) ,(self.coordinates[order[0]]), 10, 0)
        self.clock.tick(self.framerate)
        pygame.display.update()
                              
    def createOrder(self,newTruck,initial,final,goTo=None,packCode=None):
        modified = [] #create modified list to remove duplicates from path
        addList = [] #a list of location and distance in the form of (current, destination, time in distance) 
        #get path from initial to final 
        path= self.network.floyd_warshall_get_path(self.distance, self.nextn, initial, final)
        #remove duplicates
        for step in path:
            if step not in modified:
                modified.append(step) 
        #add these to list of tasks to be given to truck
        for i in xrange(len(modified)-1):
            addList.append([modified[i],modified[i+1],0,self.network.get_edge_attr(modified[i],modified[i+1],'cost'), packCode])
        newTruck.addOrder(addList,goTo) 
         
             
    def updateLocationOfTrucks(self):
        pygame.draw.rect(self.screen, (244, 238, 224), (0,0, self.screenDimension[0],self.screenDimension[1]))
        for point in self.coordinates:
            #self.screen.blit(self.house, self.coordinates[point])
            pygame.draw.circle(self.screen,(200,10,20) ,(self.coordinates[point]), 10, 0)
        for edge in self.edgeList:
            pygame.draw.lines(self.screen, (139, 69, 19), False, [self.coordinates[edge[0]],self.coordinates[edge[1]]], 2)
        for truck in self.myTrucks:
            truck.updateLocation()
            if truck.currentLocation[1] != None: #meaning that the truck has a task 
                xVal=((truck.currentLocation[2]*(self.coordinates[truck.currentLocation[1]][0]))
                      +((truck.currentLocation[3]-truck.currentLocation[2])
                        *(self.coordinates[truck.currentLocation[0]][0])))/truck.currentLocation[3]
                          
                yVal=((truck.currentLocation[2]*(self.coordinates[truck.currentLocation[1]][1]))
                      +((truck.currentLocation[3]-truck.currentLocation[2])
                        *(self.coordinates[truck.currentLocation[0]][1])))/truck.currentLocation[3]
                self.screen.blit(self.img, (xVal,yVal))
                #pygame.draw.rect(self.screen,(137,22,50),(xVal,yVal,8,5),0)
        self.clock.tick(self.framerate)
        pygame.display.update()
    
    """
    for each truck create a file  history_truckId.log
    which will save the travel history of each truck (also those which you haven't used)
    """
    def saveTravelHistoryOfAllTrucks(self):
        for truck in self.myTrucks:
            printHistory = truck.getTotalTravelHistory()
            filename = 'history/truck'+str(truck.id)+'.txt'
            f = open(filename, 'w')
            f.write("%s\n" % printHistory)
            f.close()
            