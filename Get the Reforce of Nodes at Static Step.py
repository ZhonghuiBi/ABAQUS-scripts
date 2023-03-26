#!/user/bin/python
# -*- coding:UTF-8 -*-
'''
@Author: Hs小毕
@QQ Number: 1158877067
@技术邻ID：Hs小毕
'''
#Get the Reforce of Nodes at Static Step
from visualization import *
from odbAccess import *
from abaqusConstants import *
#=============================
#Must modify the name of ODB and steps
#=============================
odbName = 'STATIC.odb'
stepName = 'Step-1'
NodeSetsName = 'RF'
#=============================
WriteFileName = 'rf.txt'
#=============================
WriteFile = open(WriteFileName,'w')
odb = openOdb(path = odbName)
myAssembly = odb.rootAssembly
frameRepository = odb.steps[stepName].frames[-1]
RefPointSet = myAssembly.nodeSets[NodeSetsName]
RForce = frameRepository.fieldOutputs['RF']
RefPointRForce = RForce.getSubset(region=RefPointSet)
RForceValues = RefPointRForce.values
for i in range(len(RForceValues)):
    Name = RForceValues[i].instance.name       #Part
    NodeLabel =  RForceValues[i].nodeLabel     #Node Label
    RfX = RForceValues[i].data[0]              #Reforce of X
    RfY = RForceValues[i].data[1]              #Reforce of Y
    RfZ = RForceValues[i].data[2]              #Reforce of Z
    WriteFile.write(str(Name) + '\t' + str(NodeLabel)+ '\t' + str(RfX)+ '\t' + str(RfY)+ '\t' + str(RfZ) + '\n')

WriteFile.close()








