import networkx as nx
import random
import matplotlib.pyplot as plt

class Network:
    def __init__(self,numberOfNodes,k):
        self.numberOfNodes=numberOfNodes
        self.k=k
        self.cometId="2021539425"
        self.trafficGraph=nx.DiGraph(directed=True)
        self.costGraph=nx.DiGraph(directed=True)
        self.linkGraph=nx.DiGraph(directed=True)
        self.cost=0
        self.numberOfEdge=0
        self.avgCost=0
        self.avgNumberOfEdge=0

    def developGraph(self):
        cometIdList=[int(num) for num in self.cometId]
        bitValueList=['#']
        for node in range(self.numberOfNodes):
            bitValueList.append(cometIdList[node%10])
        for node in range(1,self.numberOfNodes+1):
            self.trafficGraph.add_node(node)
            self.costGraph.add_node(node)
            self.linkGraph.add_node(node)
        
        for iNode in range(1,self.numberOfNodes+1):
            for jNode in range(1,self.numberOfNodes+1):
                if iNode==jNode:
                    continue
                Bij=abs(bitValueList[iNode]-bitValueList[jNode])
                self.trafficGraph.add_edge(iNode,jNode,weight=Bij)
        
        for iNode in range(1,self.numberOfNodes+1):
            edgeChoice=list(range(1,self.numberOfNodes+1))
            edgeChoice.remove(iNode)
            shortestNode=set(random.sample(edgeChoice,self.k))
            for jNode in range(1,self.numberOfNodes+1):
                if iNode==jNode :
                    continue
                if jNode  in shortestNode:
                    self.costGraph.add_edge(iNode,jNode ,weight=1)
                else:
                    self.costGraph.add_edge(iNode,jNode,weight=100)

    def findShortestPath(self):
        capacityHashMap={}
        for iNode in range(1,self.numberOfNodes+1):
            for jNode  in range(1,self.numberOfNodes+1):
                if iNode==jNode :
                    continue
                shortestPath=nx.dijkstra_path(self.costGraph, source=iNode, target=jNode )
                for curNode in range(len(shortestPath)-1):
                    src,dst=shortestPath[curNode],shortestPath[curNode+1]
                    if (src,dst) in capacityHashMap:
                        capacityHashMap[(src,dst)]+=self.trafficGraph.get_edge_data(iNode,jNode )['weight']
                    else:
                        capacityHashMap[(src,dst)]=self.trafficGraph.get_edge_data(iNode,jNode )['weight']
        for src,dst in capacityHashMap:
            if capacityHashMap[(src,dst)]!=0:
                self.numberOfEdge+=1
                self.cost+=(int(capacityHashMap[(src,dst)])*self.costGraph.get_edge_data(src,dst)['weight'])
                self.linkGraph.add_edge(src,dst,weight=int(capacityHashMap[(src,dst)]))
    
    def drawNetwork(self,k):
        plt.figure(figsize=(8,8))
        plt.title(" Network for k value = {}".format(k))
        pos = nx.spring_layout(self.linkGraph) 
        nx.draw(self.linkGraph,pos,connectionstyle='arc3, rad = 0.1',with_labels = True)
        plt.savefig("Network_graph_{}.png".format(k))
        plt.show()
def plotMetricsLineGraph(xList,yList,xLabel,yLable):
    plt.clf()
    plt.plot(xList,yList, color='red', marker='o')
    plt.title('{} vs {}'.format(yLable,xLabel), fontsize=14)
    plt.xlabel(xLabel, fontsize=14)
    plt.ylabel(yLable, fontsize=14)
    plt.grid(True)
    plt.savefig('{}_vs_{}.png'.format(yLable,xLabel))
    plt.show()

if __name__ == "__main__":       
    kValues=[]
    costList=[]
    densityList=[]
    n=21
    for k in range(3,n):
        if k>14:
            break
        kValues.append(k)
    for k in kValues:
        obj=Network(n,k)
        for _ in range(100):
            obj.cost=0
            obj.numberOfEdge=0
            obj.developGraph()
            obj.findShortestPath()
            obj.avgCost+=obj.cost
            obj.avgNumberOfEdge+=obj.numberOfEdge/(n*(n-1))
        if k in [3,8,14]:
            obj.drawNetwork(k)
        obj.avgCost=obj.avgCost/100
        obj.avgNumberOfEdge=obj.avgNumberOfEdge/100
        costList.append(obj.avgCost)
        densityList.append(obj.avgNumberOfEdge)
        print("Max cost of the network for K-value {}: ${}".format(k,obj.avgCost))
        print("Avg density of the network for K-value {}: {}".format(k,obj.avgNumberOfEdge))

    plotMetricsLineGraph(kValues,costList,"K-Values","Cost_of_Network")
    plotMetricsLineGraph(kValues,densityList,"K-Values","Network_Density")

