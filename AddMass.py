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
odbName = 'AREA.odb'
stepName = 'Step-1'
NodeSetsName = 'ADDMASS'
#=============================
WriteFileName = 'AddMass.txt'
#=============================
WriteFile = open(WriteFileName,'w')
odb = openOdb(path = odbName)
myAssembly = odb.rootAssembly
frameRepository = odb.steps[stepName].frames[-1]
RefPointSet = myAssembly.nodeSets[NodeSetsName]
RForce = frameRepository.fieldOutputs['RF']
RefPointRForce = RForce.getSubset(region=RefPointSet)
RForceValues = RefPointRForce.values
ELEM_NUM=400000
for i in range(len(RForceValues)):
    Name = RForceValues[i].instance.name       #Part
    NodeLabel =  RForceValues[i].nodeLabel     #Node Label
    RfX = RForceValues[i].data[0]              #Reforce of X
    RfY = RForceValues[i].data[1]              #Reforce of Y
    RfZ = RForceValues[i].data[2]              #Reforce of Z
    WriteFile.write("*USER ELEMENT,LINEAR,NODES=1,TYPE=U"+str(i+1)+"\n")
    WriteFile.write("\t1,2,3\n")
    WriteFile.write("*MATRIX,TYPE=MASS\n")
    WriteFile.write("\t"+str(abs(float(RfX)))+"\n")
    WriteFile.write("\t0,\t"+ str(abs(float(RfY)))+"\n")
    WriteFile.write("\t0,\t0,\t"+str(abs(float(RfZ)))+"\n")
    WriteFile.write("*ELEMENT,ELSET=ADD,TYPE=U"+str((i+1))+"\n")
    WriteFile.write("\t"+str((ELEM_NUM+i))+",\t"+str((NodeLabel))+"\n")
WriteFile.write("*Uel property,Elset=ADD,Alpha=0\n")
WriteFile.close()