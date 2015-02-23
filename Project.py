# Kyle Stoltzfus
# April 30, 2014
# This program implements an ant-colony algorithm.
# It deploys several autonomous agents onto a graph
# and then has them create equal partitions in the
# graph. This is accomplished through the use of 
# simulated pheromones placed at the vertexes.
# For more information, please refer to the paper
# that was written about this project.
# NOTE: The NetworkX Python module must be installed
# before this program will execute correctly.
# NOTE: This program can be exucuted in a terminal
# with the following command -- python Project.py

from random import randrange
import networkx as nx

# This class defines the properties of the autonomous
# agents that will partition the graph. Each agent must
# have access to this data in able for it to be able
# execute the algorithm.
class Agent:
    Number = 0
    Cycle = 0
    Controlled = []
    Possible = []
    Backtrack = []
    Current = 0
    Change = False

    def __init__(self, Number):
        self.Number = Number

# This class defines the properties of the vertexes
# of the graph. A small amount of data must be stored
# at each vertex so that the agents will know which 
# action is appropriate when they reach a particular
# vertex.
class Vertex:
    Number = 0
    Occupied = False
    Owner = 0
    Pressure = 0
    
    def __init__(self, Number):
        self.Number = Number
    

def main():
    NumberOfAgents = 6
    NumberOfVertices = 30
    NumberOfConnectedNeighbors = 3
# These first three variables can be changed to whatever parameters are
# desired for testing the program.
    AllVisited = False
    Optimal = False
    Equal = False
    Ants = []       #stores a list of the agents
    Graph = []      #stores a list of the vertices
    Connected = {}  #stores graph information in a simulated adjacency list
 
    InitializeAgents(NumberOfAgents, Ants)
    FillGraph(NumberOfVertices, Graph)
    Connected = FillConnected(NumberOfVertices, NumberOfConnectedNeighbors)
    RandomizeStart(NumberOfAgents, Ants, NumberOfVertices, Graph)
    UpdatePossible(NumberOfAgents, Ants, Connected) 
  
    while AllVisited == False or Optimal == False:
        for x in range (0, NumberOfAgents):
            BDFS(NumberOfAgents, x, Ants, Graph, Connected)

        UpdateTiming(NumberOfAgents, Ants)
        AllVisited = UpdateAllVisited(NumberOfVertices, Graph)
        Optimal = UpdateOptimal(NumberOfAgents, Ants)
        PrintCurrent(NumberOfAgents, Ants)

    PrintFinal(NumberOfAgents, Ants)

# This function initializes the autonomous agents.
# Basically, it creates the agent and gives it a number.
# It then stores the agent at that position in the list
# named Ants.
# Parameters:
# (Total) The total number of agents to be created
# (Ants) A list of the agents
def InitializeAgents(Total, Ants):
    for x in range (0, Total):
        Ant = Agent(x)
        Ants.append(Ant)

# This function initializes the vertices of the graph.
# Basically, creates the vertex and assigns it a number.
# It then stores the vertex at that position in the list
# named Graph.
# Parameters:
# (Total) The total number of vertices to be created
# (Graph) A list of the vertices
def FillGraph(Total, Graph):
    for x in range (0, Total):
        Node = Vertex(x)
        Graph.append(Node)

# This function creates the graph to be used in the program
# and creates an adjacency list for it.
# Parameters:
# (Vertices) The total number of vertices
# (NumberNeighbors) The number of neighbors each vertex is to 
# be connected to [required by the graph generator]
# Returns:
# (AdjList) An adjacency list for the graph showing which 
# vertices are connected to each other
def FillConnected(Vertices, NumberNeighbors):
    g = nx.connected_watts_strogatz_graph(Vertices, NumberNeighbors, 0)
    AdjList = {x: g.neighbors(x) for x in g.nodes()}
    return AdjList

# This function randomizes the starting positions of the
# agents. It checks to make sure the vertex is not already
# occupied by another agent. If the vertex is occupied, the 
# function will loop until an unoccupied vertex is found.
# After the starting position for an agentis determined, 
# that vertex is placed in the subgraph of the agent.
# Parameters:
# (Total) The total number of agents
# (Ants) A list of the agents
# (Vertices) The total number of vertices
# (Graph) A list of the vertices
def RandomizeStart(Total, Ants, Vertices, Graph):
    for x in range (0, Total):
        Ants[x].Controlled = []
        Random = randrange(0, Vertices)
        
        while Graph[Random].Occupied == True:
            Random = randrange(0, Vertices)
            
        Ants[x].Current = Random
        Graph[Random].Occupied = True
        Graph[Random].Owner = x
        Ants[x].Controlled.append(Ants[x].Current)
        Ants[x].Change = True
        Ants[x].Backtrack = list(Ants[x].Controlled)

# This function determines which vertices are possibilities
# for being visited next by an agent. It retrieves these 
# possibilities from the adjacency list and stores them in 
# a list for each agent.
# Parameters:
# (Total) The total number of agents
# (Ants) A list of the agents
# (Connected) A dictionary containing the adjacency list 
# of the graph
def UpdatePossible(Total, Ants, Connected): 
    for x in range (0, Total):
        Ants[x].Possible = []
        Ants[x].Possible.extend(Connected[Ants[x].Current])
       
# This function is a modified version of the depth-first search
# algorithm. The algorithm for this function is discussed in detail
# in the paper written about this project.
# Parameters: 
# (Total) The total number of agents
# (Iteration) The current agent executing the algorithm
# (Ants) A list of the agents 
# (Graph) A list of the vertices
# (Connected) A dictionary containing the adjacency list of the graph
def BDFS(Total, Iteration, Ants, Graph, Connected):
    Visited = True
    Ants[Iteration].Change = False
    
    #determine which vertex to visit next
    while len(Ants[Iteration].Possible) > 0 and Visited == True:
        if len(Ants[Iteration].Possible) > 1:
            Next = Ants[Iteration].Possible[len(Ants[Iteration].Possible) - 1]
        else:
            Next = Ants[Iteration].Possible[0]    
        
        Visited = CheckVisited(Iteration, Ants, Next)
        
        if Visited == True:
            Ants[Iteration].Possible.pop()
            
    BorderEdge = CheckBorderEdge(Next, Iteration, Graph)
    Filled = CheckFilled(Next, Total, Ants)
    
    while BorderEdge == True and Visited == False and Filled == False:
        Visited = True

        if Graph[Next].Owner != Iteration:
            P = Graph[Next].Pressure
        
            if P > 0: #pressure is greater than 0
                Prob = randrange(1, 11)
                # my simple probability function
                # This may be where the program problem exists.

                if Prob > 1:  #steal vertex from previous owner
                    Ants[Iteration].Current = Next
                    Ants[Iteration].Controlled.append(Next)
                    Ants[Iteration].Backtrack = list(Ants[Iteration].Controlled)
                    Ants[Iteration].Change = True
                    UpdatePossible(Total, Ants, Connected)
                    Graph[Next].Occupied = True
                    Temp = Graph[Next].Owner
                    Graph[Next].Owner = Iteration
                    Ants[Temp].Controlled.remove(Next)
                    return
                
            #pressure is less than or equal to 0
            #update pressure of vertex
            else:
                if len(Ants[Iteration].Controlled) == - Graph[Next].Pressure - 1:
                    Graph[Next].Pressure = 0
                
                else:
                    Graph[Next].Pressure = len(Ants[Iteration].Controlled)
            
    while BorderEdge == False and Visited == False:
        Visited = True
        
        if Graph[Next].Occupied == False: #take control of unowned vertex 
            Ants[Iteration].Current = Next
            Ants[Iteration].Controlled.append(Next)
            Ants[Iteration].Backtrack = list(Ants[Iteration].Controlled)
            Ants[Iteration].Change = True
            UpdatePossible(Total, Ants, Connected)
            Graph[Next].Occupied = True
            Graph[Next].Owner = Iteration
            return
        
    #no vertex is available to visit next
    #begin backtracking
    if len(Ants[Iteration].Backtrack) > 1:  #backtrack path exists
        Ants[Iteration].Backtrack.pop()
        Ants[Iteration].Current = Ants[Iteration].Backtrack[len(Ants[Iteration].Backtrack) - 1]
        UpdatePossible(Total, Ants, Connected)
        return
   
    else:  #no backtrack path exists
           #start new search
        Ants[Iteration].Backtrack = []
        UpdatePossible(Total, Ants, Connected)
        return

# This function checks to see if the current agent has already visited
# a vertex in the list of possible vertices to visit next. This function
# will return true or false.
# Parameters:
# (Iteration) The current agent executing the algorithm
# (Ants) A list of the agents
# (Next) The next possible vertex to visit  
def CheckVisited(Iteration, Ants, Next):
    for x in Ants[Iteration].Controlled:
        if x == Next:
            return True
    return False

# This function checks to see if the next vertex to be visited is a border
# vertex. In other words, it checks to see next vertex to be visited is 
# part of the subgraph of a different agent. This function will return 
# true or false.
# Parameters:
# (Next) The next vertex to be visited
# (Iteration) The current agent executing the algorithm
# (Graph) A list of the vertices
def CheckBorderEdge(Next, Iteration, Graph):
    if Graph[Next].Occupied == True and Graph[Next].Owner != Iteration:
        return True
    else:
        return False
                
# This function checks to see if the next vertex to be visited is 
# currently occupied by another agent. This function will return 
# true or false.
# Parameters:
# (Next) The next vertex to be visited
# (Total) The total number of agents
# (Ants) A list of the agents
def CheckFilled(Next, Total, Ants):
    for x in range (0, Total):
        if Next == Ants[x].Current:
            return True
    return False

# This function increments the cycle number of 
# each agent after it completes the BDFS function.
# Parameters:
# (Total) The total number of agents
# (Ants) A list of the agents
def UpdateTiming(Total, Ants):
    for x in range (0, Total):
        Ants[x].Cycle += 1
    
# This function checks to see if every vertex in 
# the graph has been visited. The function will return 
# true or false.
# Parameters:
# (Total) The total number of vertices
# (Graph) A list of the vertices
def UpdateAllVisited(Total, Graph):
    for x in range (0, Total):
        if Graph[x].Occupied == False:
            return False
    return True
            
# This function checks to see if an optimal solution 
# has been reached. It does this by checking if any changes
# occurred in the subgraphs of any of the agents. If no change
# has occurred, this suggests that the current solution is an 
# optimal one. This function will return true or false.
# Parameters:
# (Total) The total number of agents
# (Ants) A list of the agents
def UpdateOptimal(Total, Ants):
    for x in range (0, Total):
        if Ants[x].Change == True:
            return False
    return True
            
# This function prints information about the current cycle of the program.
# It displays the current cycle, the current position of each agent, and the 
# current number of vertices controlled by each agent.
# Parameters:
# (Total) The total number of agents
# (Ants) A list of the agents
def PrintCurrent(Total, Ants):
    print "The current cycle is {0}." .format(Ants[0].Cycle)
    for x in range (0, Total):
        print "Agent {0} controls {1} nodes." .format(Ants[x].Number, len(Ants[x].Controlled))
        print "Agent {0} is currently on node {1}." .format(Ants[x].Number, Ants[x].Current)
    
# This function prints information about the program after it has completed.
# It displays the subgraph for each agent.
# Parameters:
# (Total) The total number of agents
# (Ants) A list of the agents
def PrintFinal(Total, Ants):
    for x in range (0, Total):
        print "Agent {0} controls the following nodes: {1}." .format(Ants[x].Number, Ants[x].Controlled)


if __name__ == "__main__":
    main()
