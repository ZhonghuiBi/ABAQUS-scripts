#!/user/bin/python
# -*- coding:UTF-8 -*-
'''
@Author: Hs小毕
@QQ Number: 1158877067
@技术邻ID：Hs小毕
'''
#Get the Equivalent Node Area at Static Step
from visualization import *
from odbAccess import *
from abaqusConstants import *
import os
#=============================
#Must modify the name of ODB and steps
#=============================
odbName = 'AREA.odb'
stepName = 'Step-1'
#=============================
WriteFileNameList = ['x+shuju.txt','x-shuju.txt','y+shuju.txt','y-shuju.txt','dibushuju.txt','xshuju.txt','yshuju.txt']
NodeSetsList = ['X+','X-','Y+','Y-','Z-']
#=============================
odb = openOdb(path = odbName)
myAssembly = odb.rootAssembly
frameRepository = odb.steps[stepName].frames[-1]
RForce = frameRepository.fieldOutputs['RF']
WriteFileX = open(WriteFileNameList[-2], 'w')
WriteFileY = open(WriteFileNameList[-1], 'w')

for j in range(len(NodeSetsList)):
    WriteFile = open(WriteFileNameList[j], 'w')
    RefPointSet = myAssembly.nodeSets[NodeSetsList[j]]
    RefPointRForce = RForce.getSubset(region=RefPointSet)
    RForceValues = RefPointRForce.values
    for i in range(len(RForceValues)):
        Name = RForceValues[i].instance.name                   #Part
        NodeLabel =  RForceValues[i].nodeLabel                 #Node Label
        RfX = RForceValues[i].data[0]                          #Reforce of X
        RfY = RForceValues[i].data[1]                          #Reforce of Y
        RfZ = RForceValues[i].data[2]                          #Reforce of Z
        CoordinateZ = myAssembly.instances[Name].getNodeFromLabel(NodeLabel).coordinates[2]
        if (j == 0 or j == 1):
            if i != (len(RForceValues)-1):
                WriteFile.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfX) + '\t' + str(CoordinateZ) + '\n')
            else:
                WriteFile.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfX) + '\t' + str(CoordinateZ))
            if (j == 1) and i == (len(RForceValues)-1):
                WriteFileX.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfX) + '\t' + str(CoordinateZ))
            else:
                WriteFileX.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfX) + '\t' + str(CoordinateZ) + '\n')

        elif (j == 2 or j == 3):
            if i != (len(RForceValues) - 1):
                WriteFile.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfY) + '\t' + str(CoordinateZ) + '\n')
            else:
                WriteFile.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfY) + '\t' + str(CoordinateZ))

            if (j == 3) and i == (len(RForceValues)-1):
                WriteFileY.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfY) + '\t' + str(CoordinateZ))
            else:
                WriteFileY.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfY) + '\t' + str(CoordinateZ) + '\n')
        else:
            if i != (len(RForceValues) - 1):
                WriteFile.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfZ) + '\t' + str(CoordinateZ) + '\n')
            else:
                WriteFile.write(str(Name) + '\t' + str(NodeLabel) + '\t' + str(RfZ) + '\t' + str(CoordinateZ))

    WriteFile.close()
WriteFileX.close()
WriteFileY.close()






