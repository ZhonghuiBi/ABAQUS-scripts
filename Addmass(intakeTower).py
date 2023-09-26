# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import numpy as np

#Add Mass Distribution Coefficient
h_H0 = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
AddMassDisCoe = [0,0.33,0.44,0.51,0.54,0.57,0.59,0.59,0.60,0.60,0.60]

#Outside Rectangular Tower Shape Coefficient
a_b = [1.0/5,1.0/4,1.0/3,1.0/2,2.0/3,1.0,3.0/2,2.0,3.0,4.0,5.0]
OutRecTowShaCoe = [0.28,0.34,0.43,0.61,0.81,1.15,1.68,2.14,3.04,3.90,4.75]

Base_coordinates = 0
H0 = 42

Out_filename = 'Add_mass.txt'
odb = session.odbs['Reforce.odb']
p = mdb.models['IntakeTowerReforce'].parts['PART-1']
RE_RF = odb.steps['Step-1'].frames[1].fieldOutputs['RF']
odb.rootAssembly.nodeSets.keys() #查看全部的节点集合
Set_name = ['INNODES','OUTNODES']
#建立节点与z向坐标的字典
Nodes_label = [] #存放节点号
Nodes_coordinates = [] #存放节点z向坐标
for i in Set_name:
    Node_region=odb.rootAssembly.nodeSets[i]
    Nodes_Num = len(Node_region.nodes[0])
    for n in range(Nodes_Num):
        Nodes_label.append(Node_region.nodes[0][n].label)
        Nodes_coordinates.append(Node_region.nodes[0][n].coordinates[2])
Nodes_Dict = dict(zip(Nodes_label,Nodes_coordinates))

cpFile = open(Out_filename, 'w')
#内部节点输出
Node_region=odb.rootAssembly.nodeSets[Set_name[0]]
Nodes_Num = len(Node_region.nodes[0])
for n in range(Nodes_Num):
    NODES_RF = RE_RF.getSubset(region=Node_region).values[n]

    M_water = 0.72 * 1000 * 1* (18.0/2.0/42.0)**(-0.2)
    cpFile.write('%d\t%.6F\t%.6F\t%.6F\n' % (NODES_RF.nodeLabel,abs(NODES_RF.data[0]*M_water),abs(NODES_RF.data[1]*M_water),abs(NODES_RF.data[2]*M_water)))
    #print(NODES_RF.nodeLabel)
else:
    cpFile.close()


cpFile = open(Out_filename, 'a')
#外部节点输出
Node_region=odb.rootAssembly.nodeSets[Set_name[1]]
Nodes_Num = len(Node_region.nodes[0])
for n in range(Nodes_Num):
    NODES_RF = RE_RF.getSubset(region=Node_region).values[n]
    Node_Zcoordinates = Nodes_Dict[NODES_RF.nodeLabel]
    h = Node_Zcoordinates - Base_coordinates
    AddMassDisCoe1 = np.interp(h/H0, h_H0, AddMassDisCoe)
    OutRecTowShaCoe1 = np.interp(18.0/14.0, a_b, OutRecTowShaCoe)
    M_water = AddMassDisCoe1 * 1000 * OutRecTowShaCoe1 * (18.0 / 2.0 / 42.0) ** (-0.2)
    cpFile.write('%d\t%.6F\t%.6F\t%.6F\n' % (NODES_RF.nodeLabel,abs(NODES_RF.data[0]*M_water),abs(NODES_RF.data[1]*M_water),abs(NODES_RF.data[2]*M_water)))

else:
    cpFile.close()