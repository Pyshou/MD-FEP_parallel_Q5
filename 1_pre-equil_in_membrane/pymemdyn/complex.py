class MembraneComplex(object):
    def __init__(self, *args, **kwargs):
        self.box_height = 2.0 #Min xy
        self.box_width  = 0.8

    def setMembrane(self, membrane):
        '''Sets the membrane pdb file'''
        self.membrane = membrane
        
    def getMembrane(self):
        return self.membrane
    property(getMembrane, setMembrane)

    def setComplex(self, complex):
        '''Sets the complex object'''
        self.complex = complex
        
    def getComplex(self):
        return self.complex
    property(getComplex, setComplex)
