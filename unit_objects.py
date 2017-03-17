'''
Created on 17. mar. 2017

@author: tsy
'''

class unit(object):
    '''
    classdocs
    '''


    def __init__(self, faction=None,type=None):
        assert faction is not None
        assert type is not None
        
        self.faction = faction
        self.type = type
        
        '''unit data'''
        
        self.T = None
        self.S = None
        self.WS = None
        self.BS = None
        self.A = None
        self.SS = None
        self.W = None
        self.LD = None