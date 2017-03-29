'''
Created on 20. mar. 2017

@author: tsy
'''
import os
import xml.etree.ElementTree as ET
#import xml.etree.XMLParser as EP


filename = '2.0 Saurian Ancients.cat'

'{http://www.battlescribe.net/schema/catalogueSchema}characteristic'
cwd = os.getcwd()

os.chdir('The-9th-Age')

tree  = ET.parse(filename)
root = tree.getroot()

for line in root.iter('{http://www.battlescribe.net/schema/catalogueSchema}characteristic'):
    if line.attrib['name']=='WS':        
        print(line.attrib['name'], line.attrib['value'])
        
        

#===============================================================================
# mainChild = root[6]
#     
# 
# '''selectionEntries'''
# 
# for j,child in enumerate(mainChild):
#     
#     try:
#         child1 = child[0]
#         child2 = child1[0]
#         child3 = child2[4]
#         
#         
#         #print(child3[0].attrib['name'])
#         #print(child3[0].attrib['value'])
#         #print(child3[1].attrib['name'])
#         #print(child3[1].attrib['value'])
#     except:
#         try: 
#             child1 = child[5]
#             child2 = child1[0]
#             child3 = child2[0]
#             child4 = child3[0]
#             child5 = child4[4]
#             #===================================================================
#             # for j in range(0,12):
#             #     print(child5[j].attrib['name'])
#             #     print(child5[j].attrib['value'])
#             #===================================================================
#         except:
#             print('ERROR')
#===============================================================================