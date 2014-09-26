"""
Module for class to handle Raspberry Pi GPIO. It is the interface to the psysically world.
"""
#--------------------------------------------------------------------
#Administration Details
#--------------------------------------------------------------------
__author__ = "Mats Larse"
__copyright__ = "Mats Larsen 2014"
__credits__ = ["Mats Larsen"]
__license__ = "GPLv3"
__maintainer__ = "Mats Larsen"
__email__ = "larsen.mats.87@gmail.com"
__status__ = "Development"
__description__ = "Module for generic class to handle uart of a given intance. It makes a conenction to transmit data and recieve data. The setup of the uart are baudrate, start bits/no start bits, length of data bits and stop bits/no stop bits."
__file__ = "gpio.py"
__class__ ="IGPIO"
__dependencies__ = ["DisplayMsg"]
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
from error_display import ErrorDislay as ED # Library to display errors
import RPi.GPIO as GPIO # to rasperberry gpio library
import traceback
import os.path # Platform-independent manipulation of file names
#--------------------------------------------------------------------
#CONSTANTS
#--------------------------------------------------------------------
LOG_LEVEL = 2 # Information level
LOG_ALWAYS = 3 # Always log data
ON = 1 # ON is meaning that led is be on(light)
OFF = 1 # OFF is meaning that led is be off(no light)
GPIO_RISING = 'GPIO_RISING'
GPIO_FALLING = 'GPIO_FALLING'
GPIO_BOTH = 'GPIO_BOTH'

""" Error Messages """
WORKING = 'The intance of the ' + CLASS + ' is working without any problems and warings!!'
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

class I_GPIO(object):
    """
    Class for handling properties of the GPIO's.
    """
    class Error(Exception):
        """Exception class."""
        def __init__(self, message):
            self._message = message
            Exception.__init__(self, self._message)
        def __repr__(self):
            return self._message

    class GPIOData(object):
        """
        This class contain the data for a specific GPIO, e.q. if the GPIO is busy or not.
        """
        def __init__(self,name,operation):
            """
            Constructor of the GPIO Data.
            """
            self._name = name # Name of the given GPIO.
            self._ilde = True # True is when the GPIO is in use.
            self._operation = operation # A description of the GPIO

    def __init__(self,setup_file=None,**kwargs):
        """
        The constructor of the I_GPIO, where it setup of the interface.
        """
        
        self.__ed = ED(name='Error_GPIO',log_level=log_level)
        if kwargs[name] == str:
            self._name = kwargs[name]  # name of this instance
        elif name == None:
            pass
            
        self._log_level = log_level # Level of information
        """ARtibutes"""
        self._error_msg = WORKING # Indicate that the intance is worling fine.
        GPIO.setmode(GPIO.BOARD)
        self._pins[26]

    
    def gpio_setup(self,pin=8,io='OUTPUT',pull_up_down='DOWN'):
        """
        Set the GPIO up, depended of the pin number and input and ouput option.
        pin : is the number of the pin taken from the boardlayout.
        io : string : is the pin should act as an input or output, [INPUT,OUTPUT]
        pull_up_down : string : Deciding to use either pull-up or pull-down. This option is only possible when a pin is an input channel.
        """
        if io == 'INPUT' and pull_up_down == 'UP':
            GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        elif io == 'INPUT' and pull_up_down == 'DOWN':
            GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        elif io == 'OUTPUT' and pull_up_down == 'UP':
            GPIO.setup(pin,GPIO.OUT,pull_up_down=GPIO.PUD_UP)
        elif io == 'OUTPUT' and pull_up_down == 'DOWN':
            GPIO.setup(pin,GPIO.OUT,pull_up_down=GPIO.PUD_DOWN)
        else: 
            raise self.Error(
            'Argument [pin] has a undefined value' + self.get_name()
            +' its already running !!!  : '
            + '"{}"'.format(str(self.get_name())))
   
    def set_gpio_out(self,pin,value):
        """
        set the value of a output GPIO
        pin : is the pin number, based on the direct layout of the board.
        value : The value of the desired pin [ON,OFF]
        """
        if value == 'ON':
            GPIO.output(pin,True)
        elif value == 'OFF':
            GPIO.output(pin,False)
        else: 
            raise self.Error(
            'Could not Start Thread' + self.get_name()
            +' its already running !!!  : '
            + '"{}"'.format(str(self.get_name())))

    def get_gpio_value(self,pin):
        """
        Get value of GPIO number pin.
        pin : is the pin number, based on the direct layout of the board
        """
        return GPIO.input(pin)

    def wait_for_edge(self, pin, rfb=GPIO_RISING):
        """
        Wait for change at the pin either rising, falling or both.
        pin : is the pin number, based on the direct layout of the board.
        rfb : which kind of detection.
        """
        if rfb == GPIO_RISING:
            GPIO.wait_for_edge(pin,GPIO.RISING)
        elif rfb == GPIO_FALLING:
            GPIO.wait_for_edge(pin,GPIO.FALLING)
        elif rfb == GPIO_BOTH:
            GPIO.wait_for_edge(pin,GPIO.BOTH)
        else: 
            raise self.Error(
            'The given arguments are not satisfied for wait for egde at the GPIO. The system report an error  : '
            + '"{}"'.format(str(self.name)))

    def add_event(self,pin, rfb,func):
        """
        Add a event to deteect a specified behaviour of the GPIO by rfb and pin. If it occur the func will be called.
        pin : Int : The used pin.
        rfb : String : Rising, falling or Both.
        func : String : call back function.
        """
        if self.error != WORKING:
            raise self.Error(
                'Could not add a detection event : '
                + '"{}"'.format(str(self.name)))
        try:
            GPIO.add_event_detect(pin,GPIO.RISING,callback=func)
        except:
            raise self.Error(
                'Could not add a detection event : '
                + '"{}"'.format(str(self.name)))
            clean_up()
        log(self.__msg.getMsg(4),self._log_level)
        
    def get_name(self):
        """
        Returns the name of this intance.
        """
        return self._name
    
    def set_name(self,name):
        """
        Set a new name of this instance.
        """ 
        self._name = name
        log(self._msg.getMsg(5) + self.name)
    name = property(get_name,set_name,doc="Name Property")

    def clean_up(self):
        """
        clean up all gpios to make sure it is ready for next boot.
        """
        GPIO.cleanup()
        
    def getErrorMsg(self):
        """
        Returns the Error currently message.
        """
        return self._error_msg
    error = property(getErrorMsg, doc = 'Error Property')

    def __repr__(self):
        """
        Print the reprenstation this intance.
        """
        return '"{sdsd}"'.format(self.name)
