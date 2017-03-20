'''
Created on 17. mar. 2017

@author: tsy
'''

class unit(object):
    '''
    classdocs
    '''

    def __init__(self,excelFile=None):       

        '''object data'''
        assert excelFile is not None
        self.excelFile = excelFile
        self.readFrom = 'Excel'
        '''unit data'''

        self.faction = None
        self.name = None
                
        
        self.M = None
        self.WS = None
        self.BS = None
        self.S = None
        self.T = None
        self.W = None
        self.I = None
        self.A = None
        self.LD = None
        self.AS = None #Armorsave
        self.WS = None #Ward save        
        self.rerolls = reRolls()
        self.toroll = toRoll()
        self.special = special()


    def loadData(self,faction=None,name=None):
        assert faction is not None
        assert name is not None
        
        faction_list = ['BH','DL','DE','DH','EoS','HE','ID','KoE','OK','OaG','SA','SE','VS','UD','VC','WDG']
        assert faction in faction_list,'Wrong faction Abbreviation, options are%s'%faction_list
        
        self.faction = faction
        self.name = name


        def _load_faction_data_(self):
            assert self.faction is not None
            assert self.name is not None
            
            
            '''This should really read from battlescribe files preferably
            as a beginning I will define some "manual" input'''

            if self.readFrom is 'Excel':
                
                xl_sheet = self.faction
                xl_file = self.excelFile                
                
                from xlrd import open_workbook                            
                book = open_workbook(xl_file)      
                try:
                    s = book.sheet_by_name(xl_sheet)
                except ValueError:
                    print('Specified sheet name %s not valid' % xl_sheet)
              
                ''' Get Number of Cols and Rows'''                
                Nrows = len(s.col_types(colx=0, start_rowx=0, end_rowx=None))
                Ncols = len(s.row_types(rowx=0, start_colx=0, end_colx=None))
                
                '''find unit names from excel and check existance of unit asked for'''
                unit_names = s.col_values(colx=0, start_rowx=0, end_rowx=Nrows)
                assert any(self.name in ss for ss in unit_names), 'Unit type not found in Input'
                
                '''find row of correct unit name'''
                row_index = unit_names.index(self.name)
                
                def _load_excel_row(s=None,rowx=None,cols=None):
                    assert s is not None
                    assert rowx is not None
                    row_slice = s.row_values(rowx=rowx, start_colx=0, end_colx=cols)
                    self.M = int(row_slice[1])
                    self.WS = int(row_slice[2])
                    self.BS = int(row_slice[3])
                    self.S = int(row_slice[4])
                    self.T = int(row_slice[5])
                    self.W = int(row_slice[6])
                    self.I = int(row_slice[7])
                    self.A = int(row_slice[8])
                    self.LD = int(row_slice[9])
                    self.AS = int(row_slice[10])
                    self.WS = int(row_slice[11])
                    self.rerolls.hit = int(row_slice[12])
                    self.rerolls.wound = int(row_slice[13])
                    self.rerolls.armour = int(row_slice[14])
                    self.rerolls.ward= int(row_slice[15])
                     
                _load_excel_row(s=s,rowx = row_index,cols = Ncols)                 
        
        _load_faction_data_(self)
         
         
         
            
        
class reRolls(object):
    def __init__(self,hit=0,wound=0,armour=0,ward=0):
        self.hit = hit
        self.wound = wound
        self.armour = armour
        self.ward = ward
        
class toRoll(object):
    def __init__(self,hit=0,wound=0,armour=0,ward=0):
        self.hit = hit
        self.wound = wound
        self.armour = armour
        self.ward = ward
        
        
class special(object):
    def __init__(self,hit=0,wound=0,armour=0,ward=0):
        self.hit = hit
        self.wound = wound
        self.armour = armour
        self.ward = ward    
    

        