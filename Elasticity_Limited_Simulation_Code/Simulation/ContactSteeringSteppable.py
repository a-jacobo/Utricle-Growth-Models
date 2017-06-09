from PySteppables import *
import CompuCell
import sys

            
class ContactSteering(SteppableBasePy):
    def __init__(self,_simulator,_frequency=10):
        SteppableBasePy.__init__(self,_simulator,_frequency)
        
    def start(self):
        self.k=6.9e-2
        self.areafileHandle,self.fullFileName =self.openFileInSimulationOutputDirectory('Area.txt',"w")
        self.cellnumberfileHandle,self.fullFileName =self.openFileInSimulationOutputDirectory('NoCells.txt',"w")
        self.volumefileHandle,self.fullFileName =self.openFileInSimulationOutputDirectory('Volume.txt',"w")

        #self.surf0=0.
        #for cell in self.cellList:
        #    for neighbor , commonSurfaceArea in self.getCellNeighborDataList(cell):
        #        if neighbor == None:
        #            self.surf0+=commonSurfaceArea
    
    def step(self,mcs):    
        self.surf=0.
        self.vol=0.
        self.N=0
        for cell in self.cellList:
            self.N+=1
            self.vol=self.vol+cell.volume
            for neighbor , commonSurfaceArea in self.getCellNeighborDataList(cell):                
                if neighbor == None:
                    self.surf=self.surf+commonSurfaceArea
            
#         val=float(self.getXMLElementValue(['Plugin','Name','Contact'],['Energy','Type1','Medium','Type2','SupportingCell']))
#         print 'Adhesion Energy:', val
        #print self.surf
                #if mcs ==1400:
#        if self.N >=6000: 
#            self.k=5.1e-2
        self.val= max(10.,self.k*self.surf)
        #self.val= self.k*((self.surf-self.surf0)/self.surf0)
        self.setXMLElementValue(self.val,['Plugin','Name','Contact'],['Energy','Type1','Medium','Type2','SupportingCell'])     
        self.updateXML()   
        if mcs%50 ==0:
            print >>self.areafileHandle, mcs,self.surf
            print >>self.cellnumberfileHandle, mcs,self.N
            print >>self.volumefileHandle, mcs,self.vol
        if (self.surf == 0.) or (self.N > 30000):
            self.stopSimulation()
            