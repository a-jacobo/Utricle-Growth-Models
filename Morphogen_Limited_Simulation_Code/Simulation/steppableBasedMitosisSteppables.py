from PlayerPython import * 
import CompuCellSetup
from PySteppables import *
from PySteppablesExamples import MitosisSteppableBase
import CompuCell
import sys
from random import uniform,gauss
import math

hairCell_volume = 40
supportingCell_volume =40
div_volume = 20#supportingCell_volume/2
div_counter=500 #time since division
ref_counter=200
threshold=0.1

class DifferentiationSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        for cell in self.cellList:
            cell.targetVolume= supportingCell_volume
            cell.lambdaVolume=9.
            cellDict=self.getDictionaryAttribute(cell)
            cellDict['DivCount'] = div_counter#diff_timer
            cellDict['RefCount'] = 0.#uniform(30,ref_counter)#
            cellDict['NewlyDivided'] = 0.#False
    def step(self,mcs):
        for cell in self.cellListByType(self.SUPPORTINGCELL):
            cellDict=self.getDictionaryAttribute(cell)
            cellDict['RefCount']=max(0,cellDict['RefCount'] - 1)
            #if cellDict['DiffCount']==0:
                #if cellDict['N']<0.02:
                #    cell.type=self.HAIRCELL
                #    cell.targetVolume= hairCell_volume

class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,_simulator,_frequency=1):
        MitosisSteppableBase.__init__(self,_simulator, _frequency)
                
        # 0 - parent child position will be randomized between mitosis event
        # negative integer - parent appears on the 'left' of the child
        # positive integer - parent appears on the 'right' of the child
        self.setParentChildPositionFlag(0)       
    
    def step(self,mcs):
        cells_to_divide=[]
        field=self.getConcentrationField("GROWTH_REPRESSOR")
        #if (mcs > 1400) & (mcs <= 1500):
        #    self.EDU = True
        #else:
        #    self.EDU = False
        comPt=CompuCell.Point3D()
        for cell in self.cellListByType(self.SUPPORTINGCELL):
            cellDict=self.getDictionaryAttribute(cell)
            comPt.x=int(round(cell.xCOM))
            comPt.y=int(round(cell.yCOM))
            comPt.z=int(round(cell.zCOM))
            fv=field.get(comPt)
            if ((cell.volume > div_volume) & 
                (fv < threshold) &
                (cellDict['RefCount'] < 1)):
                cells_to_divide.append(cell)
            if (fv > threshold):
                #cell.lambdaVolume=9.
                cell.targetVolume=max(div_volume,cell.targetVolume-0.01)
        for cell in cells_to_divide:
            self.divideCellRandomOrientation(cell) #Divide cells at random orientations


    def updateAttributes(self):
        #modelFile='Simulation/DN_Collier.sbml' 
        parentCell=self.mitosisSteppable.parentCell
        childCell=self.mitosisSteppable.childCell

        pcellDict=self.getDictionaryAttribute(parentCell) #update parent dicctionary
        pcellDict['DivCount'] = div_counter
        pcellDict['RefCount'] = gauss(ref_counter,50)#uniform(20,ref_counter)
        #if self.EDU == True:
            #if uniform(0.,1.) < 0.33:
        #    pcellDict['NewlyDivided'] = 2.

        #pcellDict['NewlyDivided'] = pcellDict['NewlyDivided']/2.
        childCell.targetVolume= parentCell.targetVolume
        childCell.lambdaVolume=parentCell.lambdaVolume
        childCell.type=self.SUPPORTINGCELL
        cellDict=self.getDictionaryAttribute(childCell)
        cellDict['DivCount'] = div_counter
        cellDict['RefCount'] = gauss(ref_counter,50)#uniform(20,ref_counter)
        cellDict['NewlyDivided'] = True #pcellDict['NewlyDivided']/2.
        #self.addSBMLToCell(_modelFile=modelFile,_modelName='DN',_cell=childCell)
                
class IdFieldVisualizationSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=50):
        SteppableBasePy.__init__(self,_simulator,_frequency) 
        self.scalarCLField=self.createScalarFieldCellLevelPy("IdField")
    def step(self,mcs):
        self.scalarCLField.clear()
        for cell in self.cellList:
            cellDict=self.getDictionaryAttribute(cell)
            self.scalarCLField[cell]=cellDict['NewlyDivided']
            if cellDict['NewlyDivided'] == True: cellDict['NewlyDivided']=False
            