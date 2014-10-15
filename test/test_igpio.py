"""
Module is make for testing the I_GPIO class.
"""
__author__ = "Mats Larsen"
__copyright__ = "Mats Larsen 2014"
__credits__ = ["Mats Larsen"]
__license__ = "GPLv3"
__maintainer__ = "Mats Larsen"
__email__ = "larsen.mats.87@gmail.com"
__status__ = "Development"

#--------------------------------------------------------------------
#Import
#--------------------------------------------------------------------
from gpio import I_GPIO # Import the libray to the GPIO interface
#from msg import DisplayMsg as DM # import displayhandler
import traceback
import os # Get the api to the os
#--------------------------------------------------------------------
#CONSTANTS
#--------------------------------------------------------------------
LOG_LEVEL = 2 # Information level
LOG_ALWAYS = 1 # Always print information
FILE = 'app_detect_plastic' # Name of the file.
CLASS = 'TEST_IGPIO' # Name of the class.
MAX_STARTUPTIME = 5.0 # Maximum startup time for an instance.
#--------------------------------------------------------------------
#METHODS
#--------------------------------------------------------------------
def log(msg, log_level=LOG_LEVEL):
    """
    Print a message, and track, where the log is invoked
    Input:
    -msg: message to be printed, ''
    -log_level: informationlevel, i
    """
    global LOG_LEVEL
    if log_level <= LOG_LEVEL:
        print(str(log_level) + ' : ' + FILE + '.py::' + traceback.extract_stack()[-2][2] + ' : ' + msg)
log_level = 2
# Define the patch to the file.
setup_file = os.path.join(os.path.expanduser('~'), 'github', 'RaspberryGPIO_Python','code','GPIO_setup', 'debuggingModule_pins_setup_RPIModelB+.txt')

igpio = I_GPIO(setup_file=setup_file,name='test_GPIO',log_level=log_level)
