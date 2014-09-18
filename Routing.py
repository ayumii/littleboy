import os
import sys
import math
import json
import urllib
import Queue as queue

AdjList = []
distance = []
prev = []
path = []
directions = []
pq = queue.PriorityQueue()
url = 'http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=COM1&Level=2'
mapinfo = json.load(urllib.urlopen(url))

def createGraph():
	nodeConnectList = []
	nodeConnectVector = []
	for i in range(len(mapinfo['map'])):
		nodeId = mapinfo['map'][i]['nodeId']
		linkTo = []
                str = mapinfo['map'][i]['linkTo']
                linkTo = [int(s) for s in str.split(",")]
		nodeConnectVector.append(nodeId)
		nodeConnectVector.append(linkTo)
		nodeConnectList.append(nodeConnectVector)
		nodeConnectVector = []
		
	coordinatesNodes = []
	for i in range(len(mapinfo['map'])):
		integerPair = [mapinfo['map'][i]['x'], mapinfo['map'][i]['y']]
		coordinatesNodes.append(integerPair)

	Dist_AdjList = []
	Dist_List = []
	for i in range(len(nodeConnectList)):
		for j in range(len(nodeConnectList[i][1])):
			node = nodeConnectList[i][1][j]
			node_a_x = int(coordinatesNodes[i][0])
			node_a_y = int(coordinatesNodes[i][1])
			node_b_x = int(coordinatesNodes[int(node)-1][0])
			node_b_y = int(coordinatesNodes[int(node)-1][1])
			dist = math.sqrt(int(int(node_a_x - node_b_x)**2 + int(node_a_y - node_b_y)**2))
			Dist_List.append(dist)
		Dist_AdjList.append(Dist_List)
		Dist_List = []

	for i in range(len(nodeConnectList)):
		AdjVector = [nodeConnectList[i][0]]
		for j in range(len(nodeConnectList[i][1])):
			integerPair = [nodeConnectList[i][1][j], Dist_AdjList[i][j]]
			AdjVector.append(integerPair)
		AdjList.append(AdjVector)

def searchNodeId(nodeName):
        for i in mapinfo['map']:
                if i['nodeName'].lower() == nodeName.lower():
                        return i['nodeId']
        raise Exception("invalid location!")

def relax(u, v, w):
        u = int(u)
        v = int(v)
	if(distance[v-1] > distance[u-1] + w):
		distance[v-1] = distance[u-1] + w
		prev[v-1] = u
		integerpair = [distance[v-1], v]
		pq.put(integerpair)

def SSSP(start, end):
	for i in range(len(mapinfo['map'])):
		distance.append(sys.maxint)
		prev.append(None)
		
	distance[start-1] = 0
	
	integerPair = [distance[start-1], start]
	pq.put(integerPair)
	
	while not pq.empty():
		front = pq.get()
		if(front[0] == distance[front[1]-1]):
			for j in range(len(AdjList[front[1]-1])-1):
				relax(front[1], AdjList[front[1]-1][j+1][0], AdjList[front[1]-1][j+1][1])
	
	shortestTime = sys.maxint
	
        if distance[end-1] < shortestTime:
                shortestTime = distance[end-1]
        print "checking sequence"
        for k in range(len(distance)):
                print "distance[", k, "]", distance[k]

        backtrack = end-1
        path.append(end)
        while prev[backtrack] != None:
                path.append(prev[backtrack])
                backtrack = prev[backtrack] - 1
        
	return path

def provideDirections(nextCheckPoint):
        while True:
                pos_x, pos_y = input()
                checkPoint_x = int(mapinfo['map'][nextCheckPoint - 1]['x'])
                checkPoint_y = int(mapinfo['map'][nextCheckPoint - 1]['y'])
                dist = math.sqrt(int(int(pos_x - checkPoint_x)**2 + int(pos_y - checkPoint_y)**2))
                direction = [pos_x - checkPoint_x, pos_y - checkPoint_y]
                print direction
                if dist < 10:
                        break
        return True

createGraph()
startPlace = raw_input()
destPlace = raw_input()
try:
        startNode = int(searchNodeId(startPlace))
        destNode = int(searchNodeId(destPlace))
except Exception:
        print "INVALID!"
else:        
        path = SSSP(startNode, destNode)
        reachCheckPoint = True
        while path:
                if reachCheckPoint:
                        reachCheckPoint = False
                        nextCheckPoint = path.pop()
                        print nextCheckPoint, mapinfo['map'][nextCheckPoint-1]['nodeName']
                reachCheckPoint = provideDirections(nextCheckPoint)
