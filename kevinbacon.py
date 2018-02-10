###Driver function that implements the Kevin Bacon game using graph methods
from edgedatagraph import *
from queue import *
from minpriorityqueue import *
import sys

def createActorGraph(movieFilename):
    """Creates a graph with actors as vertices where each actor is connected to every actor they've ever been in a movie with. The title of a shared movie is associated with the edge between every pair of actors."""
    actorGraph=EdgeDataGraph()
    top250=open(movieFilename,"r")
    movieActorDict={} #Key: movie name; Value: list of movie's respective actors

    for line in top250:
        line=line.split()
        if line[0]=="Movie:":
            movieName=" ".join(line[1:]) #Variable reassigned with each movie
            movieActorDict[movieName]=[] #Empty list in which to append actors
        else:
            actor=" ".join(line[1:])
            movieActorDict[movieName].append(actor)
    
    for key in movieActorDict: #Loop to associate pair of actors to movie
        for actor1 in movieActorDict[key]:
            for actor2 in movieActorDict[key]:
                if actor1!=actor2:
                    actorGraph.addEdge(actor1,actor2,key) #Actors linked to one another
    top250.close()
    return actorGraph

def findShortestPath(graph, fromActor, toActor):
    """Returns a path using the shortest number of steps from fromActor to toActor."""
    q=Queue()
    added={} #Check if actor has been enqueued
    path={} #Link actors together for path finding
    actorNames=graph.getVertices()
    for a in actorNames:
        added[a]=False #All actors have not been enqueued yet
    q.enqueue(fromActor)
    added[fromActor]=True

    while not q.isEmpty():
        actor=q.dequeue()
        if actor==toActor: #toActor found
            pathList=[]
            pathList.append(toActor)
            vertex=path.get(actor,None) 
            while vertex!=None: #Make path list starting from end of path
                pathList.append(vertex)
                vertex=path.get(vertex,None)
            return pathList[::-1] #List must be reversed before returning

        for neighbor in graph.getAdjacentVertices(actor):
            if added[neighbor]==False: 
                q.enqueue(neighbor)
                added[neighbor]=True
                path[neighbor]=actor #Neighbor associated with current actor

    return None #If toActor is not found, there is no path

def findFamousPath(graph, fromActor, toActor, pathLength):
    """Returns the path from fromActor to toActor of length pathLength with the maximum sum of degrees of the vertices along the path."""
    shortP=len(findShortestPath(graph,fromActor,toActor)) #Shortest path length
    visited={}
    for actor in graph.getVertices():
        visited[actor]=False #All actors have not been visited yet
    return findFamousPathHelper(graph,fromActor,toActor,shortP,visited,[],0)[1] #Returns list in tuple returned by helper method

def findFamousPathHelper(graph,actor,toActor,pathLength,visited,path,degree):
    """The helper method takes 7 parameters: the graph, the starting actor, the actor to be found, the desired length of the path between the actors, a dictionary to keep track of visited actors, a list to append actors to create possible paths, and the degree sum. A tuple containing the highest sum of degrees and the respective path list is returned."""
    path.append(actor)
    visited[actor]=True
    degree+=len(graph.getAdjacentVertices(actor)) #Recur calls increment degree
    if len(path)==pathLength and actor==toActor: #Path is appropriate length and toActor found
        pathCopy=path[:] #Must copy full path before popping to return
        path.pop()
        visited[actor]=False #Allows actor to be used for other paths
        return (degree,pathCopy)
    elif len(path)==pathLength and actor!=toActor: #Path is appropriate length but toActor not found
        path.pop()
        visited[actor]=False
        return (0,None) #Invalid path
    else: #Continue with DFS
        highest=(0,None)
        for neighbor in graph.getAdjacentVertices(actor):
            if visited[neighbor]==False:
                pathRecur=findFamousPathHelper(graph,neighbor,toActor,pathLength,visited,path,degree) #Recursive call returns (degree sum,path) tuple 
                if pathRecur[0]>highest[0]:
                    highest=pathRecur #Record the highest degree sum
        path.pop()
        visited[actor]=False
        return highest #Return the tuple with the highest degree sum

def getDistanceDistribution(graph, actor):
    """Returns a list where each element i contains the number of vertices i steps away from the given vertex."""
    q=Queue()
    added={}
    levelDict={} #Each vertex is assigned a level number that indicates their distance from the given actor
    distList=[1] #Level 0 only has the given actor
    count,level=0,1 #Start level at 1
    
    actorNames=graph.getVertices()
    for a in actorNames:
        added[a]=False
        levelDict[a]=None #Initiate all actors' levels to 'None'

    q.enqueue(actor)
    added[actor]=True
    levelDict[actor]=0 #The given actor is level 0
    priorActor=actor #Used to compare actor levels in following loop

    while not q.isEmpty():
        currentActor=q.dequeue()
        adjacentActors=graph.getAdjacentVertices(currentActor)
        if levelDict[currentActor]>levelDict[priorActor]: #Check level values
            distList.append(count) #At new level, so append count
            count=0 #And reset accumulator
            level+=1
        for neighbor in adjacentActors:
            if added[neighbor]==False: #If neighbor was not already discovered
                q.enqueue(neighbor)
                added[neighbor]=True
                levelDict[neighbor]=level #Assign level value to neighbor
                count+=1
        priorActor=currentActor #Update prior actor
    return distList

def findObscurePath(graph, fromActor, toActor):
    """Returns the path from fromActor to toActor that has the smallest sum of degrees amongst the vertices in the path."""
    degree={}
    previous={}

    actors=graph.getVertices()
    for a in actors:
        degree[a]=sys.maxsize #Initialize all actor degrees to large number
        previous[a]=None #Initialize previous actor
        
    degree[fromActor]=0 #Degree of fromActor to itself is 0
    previous[fromActor]=None #Also set as the previous actor

    minQueue=MinPriorityQueue(actors,[degree[a] for a in actors])

    for x in actors:
        curActor=minQueue.dequeue() #Actor with lowest degree
        for neighbor in graph.getAdjacentVertices(curActor):
            newDegree=degree[curActor]+len(graph.getAdjacentVertices(neighbor)) #Neighbor's degree added to current actor's degree
            if degree[neighbor]>newDegree:
                minQueue.decreasePriority(neighbor,degree[neighbor],newDegree) #Update neighbor's priority
                degree[neighbor]=newDegree #Change degree to lower value
                previous[neighbor]=curActor #Previous of neighbor is the current actor
    path=[]
    if degree[toActor]<sys.maxsize: #If path exists, toActor's degree <infinity
        path=[toActor]
        priorActor=previous[toActor]
        while priorActor!=None: #Construct path list
            path.append(priorActor)
            priorActor=previous[priorActor]
        return path[::-1] #Reverse path before returning
    return None #Otherwise no path exists

def actorInput(graph):
    """Keeps asking the user for a name until the name is in the database."""
    vertices = graph.getVertices()
    actor = input("Actor's name: ")
    while actor not in vertices:
        actor = input("Actor not in the database. Please select another: ")
    return actor

def printPath(graph, path):
    """Takes a path of actors and prints it out nicely."""
    for i in range(len(path) - 1):
        print(str(path[i]) + " and " + str(path[i + 1]) + " were in " + str(graph.getEdgeData(path[i], path[i + 1])))

def main():
    """Plays the Kevin Bacon game!"""
    print("Creating actor graph...")
    g = createActorGraph('top250.txt')
    
    center = "Kevin Bacon"
    quit = False
    while not quit:
        print("="*(len(center) + 19))
        print("Current center is: " + center)
        print("="*(len(center) + 19))
        print("s) Get statistics for the center")
        print("p) Find a path to another actor")
        print("f) Find a famous path to another actor")
        print("o) Find an obscure path to another actor")
        print("c) Change the center")
        print("q) Quit")

        userChoice = input("Please select an option: ")
        while userChoice not in ['p', 's', 'f', 'o', 'c', 'q']:
            print("Option not recognized, please type p, s, f, o, c, or q")
            userChoice = input("Please select an option: ")

        if userChoice == 'p':
            toActor = actorInput(g)
            path = findShortestPath(g, center, toActor)
            if path == None:
                print("No path found!")
            else:
                print(str(toActor) + "'s " + center + " number is: " + str(len(path) - 1))
                printPath(g, path)
        elif userChoice == 's':
            distanceDistribution = getDistanceDistribution(g, center)
            sumDist = 0
            totalConnected = 0
            for i in range(len(distanceDistribution)):
                sumDist += i*distanceDistribution[i]
                totalConnected += distanceDistribution[i]
            print("Average distance: " + str(sumDist/totalConnected))
            print("Max distance: " + str(len(distanceDistribution) - 1))
            print("Percent connected: " + str(100*totalConnected/len(g.getVertices())))
        elif userChoice == 'f':
            toActor = actorInput(g)
            shortestPath = findShortestPath(g, center, toActor)
            if shortestPath == None:
                print("No path found!")
            else:
                famousPath = findFamousPath(g, center, toActor, len(shortestPath))
                printPath(g, famousPath)
    
        elif userChoice == 'o':
            toActor = actorInput(g)
            obscurePath = findObscurePath(g, center, toActor)
            if obscurePath == None:
                print("No path found!")
            else:
                printPath(g, obscurePath)
        elif userChoice == 'c':
            center = actorInput(g)
        elif userChoice == 'q':
            quit = True
        input("(hit enter to continue)")

main()
