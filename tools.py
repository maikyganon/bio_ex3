import csv
import random
import sys
import numpy as np

'''
extracts data from csv to two dimension array
'''
def getArrOfVectorByCSVName(csvName):
    #The returned array is 1d-array that its first index is an array of the cols.
    array=[]
    with open(csvName) as file_name:
        file_read = csv.reader(file_name)
        array = list(file_read)
    #print(array)
    arrayOfArrays = [v[1:] for v in array[1:]]
    #turn each inner array to array of integers
    for k,arr in enumerate(arrayOfArrays):
        arrayOfArrays[k] = [int(x) for x in arr]
    return arrayOfArrays

'''
norms the inputsArr in MinMax method
'''
def normInputs(inputsArr):
    minVec, maxVec = getMinMaxVectorsOfInputs(inputsArr)
    for arr in inputsArr:
        for i, item in enumerate(arr):
            if i > 1:
                arr[i] = (arr[i] - minVec[i]) / (maxVec[i] - minVec[i])
    print(inputsArr)

'''
norms the inputsArr in z_score method
'''
def Z_ScoreNormalization(inputsArr):
    npInputsArr=np.float32(np.array(inputsArr))
    epsilon = sys.float_info.epsilon
    for i in range(len(npInputsArr[0])):
        if (i>1):
            v=npInputsArr[:,i]
            npInputsArr[:, i]=(npInputsArr[:,i]-np.mean(v))/(np.std(v)+epsilon)
    for i,arr in enumerate(inputsArr):
        for j in range(len(arr)):
            inputsArr[i][j]=npInputsArr[i][j]
    return

'''
For every row in inputArr change the value of the elements to element divided by the second element in the row.
the second element in the row is Total votes. 
'''
def norm_zero_to_one(inputsArr):
    for arr in inputsArr:
        for i,item in enumerate(arr):
            if i > 1:
                arr[i] = arr[i] / arr[1]

def generateRandomNumberInLimitedRange(low,high):
    return random.sample(range(low, high+1), 1)[0]

'''
returns min and max vectors of the features in the vectors of inputsArr
meaning that for inputsArr[[1,2,3],[0,1,50]]
minVec=[0,1,3]
maxVec=[1,2,50] 
'''
def getMinMaxVectorsOfInputs(inputsArr):
    maxVec=[0]*len(inputsArr[0])
    for arr in inputsArr:
        for k,field in enumerate(arr):
            if (field>maxVec[k]):
                maxVec[k]=field
    minVec=maxVec.copy()
    for arr in inputsArr:
        for k,field in enumerate(arr):
            if (field<minVec[k]):
                minVec[k]=field
    return minVec,maxVec

def createAndAddRandomVectorToEachHexagon(hexagons, inputsArr):
    minVec, maxVec = getMinMaxVectorsOfInputs(inputsArr)
    for hexagon in hexagons:
        hexagon.addRepresentedVector([random.uniform(minVec[i], maxVec[i]) for i in range(len(inputsArr[0]))])

'''
returns "almost" euclidean distance between two vectors-
meaning, that the first two features are being ignored in the summation.
'''
def distance(v1,v2) -> int:
    sigmaVector = [(v2[k]-v1[k])**2 for k in range(len(v2))]
    sum=0
    for i,field in enumerate(sigmaVector):
        if (i>1):
            sum+=field
    return sum

'''
This method returns the closest hexagon to the vector x.
using the function distance.
'''
def findClosestHexagonIndex(x, hexagons):
    minIndex=0
    minDistance=sys.maxsize
    for k,hexagon in enumerate(hexagons):
        temp = distance(x,hexagon.representedVector)
        if(temp < minDistance):
            minDistance = temp
            minIndex=k
    return minIndex

'''
Calculate The average distance d between an input vector and the neuron that represents it.
'''
def calcQuantErrorScore(hexagons):
    totalErr = 0
    countValidHexagons = 0
    for hex in hexagons:
        hexErr = 0
        for data_row in hex.cluster:
            hexErr += distance(data_row, hex.representedVector)
        if len(hex.cluster) > 0:
            totalErr += hexErr / len(hex.cluster)
            countValidHexagons += 1
    return totalErr / countValidHexagons

'''
Shuffel the rows in inputsArr.
return new array.
'''
def shuffleRows(inputsArr):
    rowsNewOrder=random.sample(range(0,len(inputsArr)),len(inputsArr))
    newInputsArr=[]
    for i in rowsNewOrder:
        newInputsArr.append(inputsArr[i])
    return newInputsArr

'''
All the logic's for every epoch
'''
def doEpoch(hexagons,inputsArr):
    for h in hexagons:
        h.cluster.clear()
    for x in inputsArr:
        k = findClosestHexagonIndex(x, hexagons)
        hexagons[k].cluster.append(x)
        hexagons[k].updateHexagonVector(x,hexagons)
    for hexagon in hexagons:
        hexagon.updateColour()
        hexagon.isColourValid=0
    return
