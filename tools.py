import csv
import random
import sys

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

def generateRandomNumberInLimitedRange(low,high):
    return random.sample(range(low, high+1), 1)[0]

def createAndAddRandomVectorToEachHexagon(hexagons, inputsArr):
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
    for hexagon in hexagons:
        hexagon.addRepresentedVector([generateRandomNumberInLimitedRange(minVec[i],maxVec[i]) for i in range(len(inputsArr[0]))])

def distance(v1,v2) -> int:
    sigmaVector = [(v2[k]-v1[k])**2 for k in range(len(v2))]
    sum=0
    for field in sigmaVector:
        sum+=field
    return sum



def findClosestHexagonIndex(x, hexagons):
    minIndex=0
    minDistance=sys.maxsize
    for k,hexagon in enumerate(hexagons):
        if(distance(x,hexagon.representedVector) < minDistance):
            minIndex=k
    return k


def doEpoch(hexagons,inputsArr):
    for x in inputsArr:
        k = findClosestHexagonIndex(x, hexagons)
        hexagons[k].updateHexagonVector(x)
    return 0









# raise an error because not all the fields are numbers !!
# import numpy as np
# def getArrOfVectorByCSVName(csvName):
#     array=[]
#     with open(csvName) as file_name:
#         array = np.loadtxt(file_name, delimiter=",")
#     print(array)
#     return array


