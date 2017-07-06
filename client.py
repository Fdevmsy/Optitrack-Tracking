from NatNetClient import NatNetClient
import configparser
import numpy as np
from collections import deque
#import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
from scipy.sparse import csr_matrix
from struct import *
import socket  
import time
starttime=time.time()

configParser = configparser.ConfigParser(allow_no_value=True)
configParser.read('config.ini')
numFrame = 0


# This is a callback function that gets connected to the NatNet client and called once per mocap frame.
def receiveNewFrame( inMarkerModelName, inMarkerset, markerCount, frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                    labeledMarkerCount, latency, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
    pass

def receiveRigidBodyFrame( id, position, rotation ):
    pass

def unlabeledMarkerFrame(u_unlabeled):    
    pos_roate = compute_Pos_Angle(u_unlabeled)
    
    if configParser.get('positionConfig', 'printFramesCount') == "True":
        countFrame()
    
    if configParser.get('positionConfig', 'printObejctsCount') == "True":
        print("Obejcts count", len(pos_roate), end="\r") 
        
    if configParser.get('positionConfig', 'printData') == "True":
        print(pos_roate)
        
    if configParser.get('positionConfig', 'sendSocket') == "True":
        if pos_roate is not -1:      
            sendSocket(pos_roate)
    #        pass
        else:
            print("There's no pair\n")

def countFrame():
    global numFrame
    global starttime 
    if numFrame == 0:
        starttime = time.time()
    numFrame = numFrame + 1
    if time.time() - starttime > 1:
        print("Frame Rate:", numFrame, end = '\r')
        numFrame = 0;
    
def NNeighbor(mat):
    idx = list()
    distMatrix = euclidean_distances(mat)
    distMatrix = csr_matrix(distMatrix)
    # the max distance between a pair of points 
    maxDistance = float(configParser.get('positionConfig', 'maxDistance'))
#    maxDistance = 0.05
    for i in range(distMatrix.shape[0]):
        row = distMatrix.getrow(i).toarray()[0].ravel()
        top_indices = row.argsort()[1]
        top_values = row[row.argsort()[1]]
        if top_values > maxDistance:
            idx.append(-1)
        else:
            idx.append(top_indices)
    return idx

def trace( *args ):
    pass 
#    print( "".join(map(str,args)) )

def compute_Pos_Angle(posData):
#    unlabeled_markers = ([[1, 1, 0.1], [-2, -2, 0.2], [7, 0., 0.1], 
#                         [1, 2, 0.3],[-3, -2, 0.4],[8, 1, 0.2]])
    unlabeled_markers = posData
    n_unlabled_markers = np.array(unlabeled_markers)

    trace("raw markers:")
#    trace(n_unlabled_markers[:,0:3])
    if len(n_unlabled_markers) < 2:
        return -1
    else:
        markers_index = NNeighbor(n_unlabled_markers[:,0:2])
        trace("neighbor markers index:")
        trace(markers_index)

        # marker_set contains all the pairs of ID collected. 
        markers_set = [] 

        for i in range(len(markers_index)):
            if(markers_index[i] > i):
                markers_set.append([i, markers_index[i]])

        n_markers_set = np.array(markers_set)
        trace("markers set:")
        trace(markers_set)

        front_markers_set = list()
        back_markers_set = list()
        for i, j in markers_set:
            if n_unlabled_markers[i][2] > n_unlabled_markers[j][2]:
                front_markers_set.append(i)
                back_markers_set.append(j)
            else:
                front_markers_set.append(j)
                back_markers_set.append(i)
        # print(front_markers)

        back_markers = (n_unlabled_markers[back_markers_set])[:,0:2]
        front_markers = (n_unlabled_markers[front_markers_set])[:,0:2]
        trace("back markers:")
        trace(back_markers)
        trace("font markers:")
        trace(front_markers)

        robot_location = (back_markers+front_markers)/2
        trace("robot location:")
        trace(robot_location)

        delta_points = front_markers - back_markers
        robot_theta = (np.arctan2(delta_points[:,1], delta_points[:,0])+np.pi*2) % (np.pi*2)
        trace("robot theta:")
        trace(robot_theta)

        trace("robot_data:")
        robot_data = np.hstack((robot_location, robot_theta.reshape(robot_theta.shape[0],1)))
        trace(robot_data)
        if len(robot_data) == 0:
            return -1 
        else:                    
            return robot_data

def sendSocket(pos_angle):
    s = socket.socket()         # Create a socket object
    host = configParser.get('socketInfo', 'severIP')
    port = int(configParser.get('socketInfo', 'port'))        
#    data = np.random.rand(4,4)
    data = pos_angle
    newString = ''
    for row in data:
        rowString = ",".join(map(str, row))
        newString = newString + rowString + '\r\n'
    newString = newString.encode()
    lenth = len(newString)+6
#    print(lenth)
    lenth = pack('<i',  lenth)
#    print(newString)
    try:
        s.connect((host, port))		        
        try:                                    
            header = bytes([0x4a, 0x44, 0x43, 0x43, 0x09]) + lenth
            s.sendall(header)
            s.sendall(newString)  
#            print(newString)                             
        except:
            print("send failed")
            
    except:
#        print("Disconnected!\n")
        pass
    
# This will create a new NatNet client
streamingClient = NatNetClient()

# Configure the streaming client to call our rigid body handler on the emulator to send data out.
streamingClient.newFrameListener = receiveNewFrame
streamingClient.rigidBodyListener = receiveRigidBodyFrame
streamingClient.unlabeledMarkerListener = unlabeledMarkerFrame
# Start up the streaming client now that the callbacks are set up.
# This will run perpetually, and operate on a separate thread.

streamingClient.run()
#ani = animation.FuncAnimation(fig, update, interval=100)
#plt.show()






