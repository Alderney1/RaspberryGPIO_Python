#--------------------------------------------------------------------
#Administration Details
#--------------------------------------------------------------------
__author__ = "Mats Larsen"
__copyright__ = "Mats Larsen 2014"
__credits__ = ["Mats Larsen"]
__license__ = "GPLv3"
__maintainer__ = "Mats Larsen"
__email__ = "larsen.mats.87@gmail.com"
__status__ = "Development"
__description__ = "Module to handle platform for the running device."""
__file__ = "plarform.py"
__class__ ="Platform"
__dependencies__ = "DisplayMsg"
#--------------------------------------------------------------------
#Version
#--------------------------------------------------------------------
__version_stage__ = "Pre_alpha"
__version_number__ = "0.1"
__version_date__ = "20140917"
__version_risk__ = "This current version is in Pre-alpha version, which meaning that the program can crash or perform other unrespected behavoiurs."
__version_modification__ = "The development project has just been created."
__version_next_update__ = "Implementation of connection."
#--------------------------------------------------------------------
#Hardware
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#Import
#--------------------------------------------------------------------
#from error_display import ErrorDislay as ED # Library to display errors
import traceback # module to extrat, format and print stack traces of python programs
import os.path # Platform-independent manipulation of file names
from msg import DisplayMsg as DM # import displayhandler
from loadfile import LoadFile as LF # import load file class
import platform # import the platform of the running system.
import re
from error_display import ErrorDisplay as ED # import the display error
#--------------------------------------------------------------------
#CONSTANTS
#--------------------------------------------------------------------
LOG_LEVEL = 2 # Information level
LOG_ALWAYS = 3 # Always log data
file_error = setup_file = os.path.join(os.path.expanduser('~'), 'github', 'RaspberryGPIO_Python','code','messages', 'error_list.txt')

ERROR_LEVEL = False # level of the error
RASPBERRY_PI = 'RASPBERRY_PI'
BEAGLEBONE_BLACK = 'BEAGLEBONE_BLACK'
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
        print(str(log_level) + ' : ' + __file__ + '.py::' + traceback.extract_stack()[-2][2] + ' : ' + msg)

class Platform(object):
    """
    Class of the running platform, to handle infomations.
    """
    def __init__(self, **keywords):
        """
        The constructor of the plarform class.
        """
        self._name = keywords.get('name','platform Information')
        self._log_level = keywords.get('log_level',2)
        self._error_level = keywords.get('error_level',False)
        self._platform_name = self.detect_platform()
        
        
        if ERROR_LEVEL == True:
            self._ed = ED(self._name + ' ErrorDisplay')

    def detect_platform(self):
        """
        Detect the running system of the device. The platform type will be returned.
        Inputs-> None
        Return -> int : The platform of the system, False for error.
        """
        p = platform.platform()

        #Platform output on Raspbian testing/jessie ~May 2014:Linux-3.10.25+-armv6l-with-debian-7.4
        if plat.lower().find('armv6l-with-debian') > -1:
            return RASPBERRY_PI

        elif plat.lower().find('raspberry_pi') > -1: # Handle pidora distribution.
            return RASPBERRY_PI
    
        elif plat.lower().find('arch-armv6l') > -1: # Handle arch distribution.
            return RASPBERRY_PI
    
        #Handle Beaglebone Black, Platform output on Debian ~May 2014: Linux-3.8.13-bone47-armv7l-with-debian-7.4
        elif plat.lower().find('armv7l-with-debian') > -1:
             return BEAGLEBONE_BLACK
        #Handle Beaglebone Black, Platform output on Ubuntu ~July 2014: Linux-3.8.13-bone56-armv7l-with-Ubuntu-14.04-trusty
        elif plat.lower().find('armv7l-with-ubuntu') > -1:
            return BEAGLEBONE_BLACK	
        elif plat.lower().find('armv7l-with-glibc2.4') > -1:
            return BEAGLEBONE_BLACK
        else:
            return False

    def pi_revision(self):
        """Detect the revision number of a Raspberry Pi, useful for changing
        functionality like default I2C bus based on revision."""
        # Revision list available at: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
        with open('/proc/cpuinfo', 'r') as infile:
            for line in infile:
                # Match a line of the form "Revision : 0002" while ignoring extra
                # info in front of the revsion (like 1000 when the Pi was over-volted).
                match = re.match('Revision\s+:\s+.*(\w{4})$', line)
                if match and match.group(1) in ['0000', '0002', '0003']:
                    # Return revision 1 if revision ends with 0000, 0002 or 0003.
                    return 1
                elif match:
                    # Assume revision 2 if revision ends with any other 4 chars.
                    return 2
            # Couldn't find the revision, throw an exception.
                raise RuntimeError('Could not determine Raspberry Pi revision.')

    def __repr__(self):
        """
        Print all settings of this instance.
        """
        return '---------------------------------------------------------- \nAdministration Details:\nAuthor: %s, copyright: %s, Credits: %s, License: %s, Maintainer: %s, Email: %s, Status: %s, Description: %s, Class: %s, File: %s, Dependencies: %s \n---------------------------------------------------------- \nVersion: \nVersion stage: %s, Version number: %s, Version date: %s, Version risk: %s, Version modification: %s, Version next update: %s \n---------------------------------------------------------- \nArtibutes:' % (__author__,__copyright__,__credits__,__license__,__maintainer__,__email__,__status__,__description__,__file__,__class__,__dependencies__,__version_stage__,__version_number__,__version_date__,__version_risk__,__version_modification__,__version_next_update__)

