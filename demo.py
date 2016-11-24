# -*- coding: utf-8 -*-
from __future__ import print_function
import TreeStructureModule as tsm


path = u'C:\\Users\\Jakub\\Desktop\\studia ZUT zima 2016 - 2017\\struktury danych\\wykłady\\3'

treee = tsm.Tree_Structure('sieci', tsm.Tree_Structure.generateTreeStructure(path), path)


treee.printTree()

raw_input('pls press enter to continue..')

list = tsm.Tree_Structure.compareTreeStructures(treee.tree_structure, tsm.Tree_Structure.generateTreeStructure(treee.path))

for item in list:
    print(item.name)
    print(item.path)
    print ()
