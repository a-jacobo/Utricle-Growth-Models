import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])
sys.path.append(environ["SWIG_LIB_INSTALL_DIR"])

import CompuCellSetup

sim,simthread = CompuCellSetup.getCoreSimulationObjects()
CompuCellSetup.initializeSimulationObjects(sim,simthread)
import CompuCell #notice importing CompuCell to main script has to be done after call to getCoreSimulationObjects()

#Add Python steppables here
from PySteppablesExamples import SteppableRegistry
steppableRegistry=SteppableRegistry()

from steppableBasedMitosisSteppables import DifferentiationSteppable
differentiationSteppable=DifferentiationSteppable(sim,1)
steppableRegistry.registerSteppable(differentiationSteppable)

from steppableBasedMitosisSteppables import MitosisSteppable
mitosisSteppable=MitosisSteppable(sim,1)
steppableRegistry.registerSteppable(mitosisSteppable)

from ContactSteeringSteppable import ContactSteering
contactSteetingSteppable=ContactSteering(sim,10)
steppableRegistry.registerSteppable(contactSteetingSteppable)

from steppableBasedMitosisSteppables import IdFieldVisualizationSteppable
idFieldSteppable=IdFieldVisualizationSteppable(sim,10)
steppableRegistry.registerSteppable(idFieldSteppable)

CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)




