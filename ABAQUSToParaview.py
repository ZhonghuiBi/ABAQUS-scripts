#!/user/bin/python
# -*- coding:UTF-8 -*-
'''
@Author: Hs小毕
@QQ Number: 1158877067
@技术邻ID：Hs小毕
'''
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from odbAccess import *
import numpy as np
p = mdb.models['Model-1'].parts['Part-1']
#Get total number of elements
ElementsTotalNumber = len(p.elements)
#Get total number of nodes
NodesTotalNumber = len(p.nodes)
#One dimensional array to reserve elements label
ElementsLabel = np.ones(shape=(ElementsTotalNumber), dtype=np.int)
#One dimensional array to reserve nodes label
NodesCoordinates = np.ones(shape=(NodesTotalNumber,3), dtype=np.int)
#Two dimensional array to reserve nodes label
ElementsNodeLabel = np.ones(shape=(ElementsTotalNumber,4), dtype=np.int)

for i in range(NodesTotalNumber):
    NodesCoordinates[i, 0] = p.nodes[i].coordinates[0]
    NodesCoordinates[i, 1] = p.nodes[i].coordinates[1]
    NodesCoordinates[i, 2] = p.nodes[i].coordinates[2]

for i in range(ElementsTotalNumber):
    #The nodes associated with elements are counterclockwise order
    Index0 = p.elements[i].connectivity[0]
    ElementsNodeLabel[i,0] = p.nodes[Index0].label
    Index1 = p.elements[i].connectivity[1]
    ElementsNodeLabel[i,1] = p.nodes[Index1].label
    Index2 = p.elements[i].connectivity[2]
    ElementsNodeLabel[i,2] = p.nodes[Index2].label
    Index3 = p.elements[i].connectivity[3]
    ElementsNodeLabel[i,3] = p.nodes[Index3].label


#Obtain the displacement of x and y
NodesDisplacement = np.ones(shape=(NodesTotalNumber,3), dtype=np.float)
odb = openOdb(path='Dynamic-SV-20.odb')
field = odb.steps['Step-2'].frames[250].fieldOutputs['U']

print(NodesDisplacement[0, 1])

for i in range(NodesTotalNumber):
    NodesDisplacement[i, 0] = field.values[i].data[0]
    NodesDisplacement[i, 1] = field.values[i].data[1]
    NodesDisplacement[i, 2] = 0


cpFile = open('Displacement.vtk', 'w')
cpFile.write('# vtk DataFile Version 2.0\n')
cpFile.write('Oblique case\n')
cpFile.write('ASCII\n')
cpFile.write('DATASET UNSTRUCTURED_GRID\n')
cpFile.write('POINTS\t'+str(NodesTotalNumber)+'\tfloat\n')
for i in range(NodesTotalNumber):
    cpFile.write(str(NodesCoordinates[i,0])+'\t'+str(NodesCoordinates[i,1])+'\t'+str(NodesCoordinates[i,2])+'\n')

cpFile.write('CELLS\t'+str(ElementsTotalNumber)+'\t'+str(ElementsTotalNumber*5)+'\n')

for i in range(ElementsTotalNumber):
    cpFile.write(str(4)+'\t'+str(ElementsNodeLabel[i,2]-1)+'\t'+str(ElementsNodeLabel[i,3]-1)+'\t'+str(ElementsNodeLabel[i,0]-1)+'\t'+str(ElementsNodeLabel[i,1]-1)+'\n')

cpFile.write('CELL_TYPES\t'+str(ElementsTotalNumber)+'\n')

for i in range(ElementsTotalNumber):
    cpFile.write(str(9)+'\n')

cpFile.write('POINT_DATA\t'+str(NodesTotalNumber)+'\n')
cpFile.write('VECTORS Displacement float \n')
for i in range(NodesTotalNumber):
    cpFile.write(str(round(NodesDisplacement[i, 0],2))+'\t'+str(round(NodesDisplacement[i, 1],2))+'\t'+str(round(NodesDisplacement[i, 2],2))+'\n')

cpFile.close()