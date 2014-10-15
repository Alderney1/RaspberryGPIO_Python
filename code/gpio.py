"""
Module for class to handle Raspberry Pi GPIO. It is the interface to the psysically world.
"""
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
#from error_display import ErrorDislay as ED # Library to display errors
import RPi.GPIO as GPIO # to rasperberry gpio library
import traceback # module to extrat, format and print stack traces of python programs
import os.path # Platform-independent manipulation of file names
from msg import DisplayMsg as DM # import displayhandler
from loadfile import LoadFile as LF # import load file class
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

PIN_STATE = ['Ilde', 'Busy']

""" Error Messages """
WORKING = 'The intance of the ' + __class__ + ' is working without any problems and warings!!'
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

class BaseGPIO(object):
    """
    Class for handling properties of the GPIO's.
    """
    class GPIOData(object):
        """
        This class contain the data for a specific GPIO, e.q. if the GPIO is busy or not.
        """
        def __init__(self,name,gpio_id,properties,state,io,pull,operation):
            """
            Constructor of the GPIO Data.
            """
            self._name = name # Name of the given GPIO.
            self._id = gpio_id # ID of the gpio
            self._properties = properties # The properties of the gpio
            self._state = state # True is when the GPIO is in use.
            self._io = io # IO configuration of the gpio
            self._pull = pull #Pull configration of the pin.
            self._operation = operation # A description of the GPIO
            
        def get_name(self):
            """
            Return the name of the PIN.
            """
            return self._name

        def set_name(self,name):
            """
            Set new name of the PIN.
            """
            self._name = name
        name = property(get_name,set_name,doc='Name Property')

        def __repr__(self):
            """
            Print the reprenstation this intance.
            """
            return '"{sdsd}"'.format(self.name)


    def __init__(self,setup_file=None,**kwargs):
        """
        The constructor of the I_GPIO, where it setup of the interface.
        Inputs:
        name-> Str : Describe the name of the instance.
        """
        #Argument assignment
        if setup_file != None and type(setup_file) == str:
            self._setup_file = setup_file
        else:
            pass

        self._name = kwargs.get('name','IGPIO_RPI')
        self._log_level = kwargs.get('log_level',LOG_LEVEL) # Level of information

        
        if type(self._name) != str:
            pass
        
        #innerassignment
        self._dm = DM()

        #self.__ed = ED(name='Error_GPIO',log_level=self._log_level) # Error handling
            
        """ARtibutes"""
        self._error_msg = WORKING # Indicate that the intance is worling fine.
        GPIO.setmode(GPIO.BOARD)
        self._file_gpio = LF(name='File_GPIO',path=self._setup_file,comment='#',col_number=7)
        
       
        log('GPIO is initiliaed')
    
    def load_pin_configuration(self):
        """
        Load the configuration file.
        """
        #set gpio setupts into the gpip layer.
        self._pins = []
        load_data = self._file_gpio.data
        for i in range(0,39):
            print(load_data[i][1])
            self._pins.append(self.GPIOData(name=load_data[i][0],gpio_id=load_data[i][1],properties=load_data[i][2],state=load_data[i][3],io=load_data[i][4],pull=load_data[i][5],operation=load_data[i][6]))
            if load_data[i][3] == PIN_STATE[1]:
                self.gpio_setup(pin=load_data[i][1],io=load_data[i][4],pull_up_down=load_data[i][5])

    
    def gpio_setup(self,pin=8,io='OUTPUT',pull_up_down='Pull_DOWN'):
        """
        Set the GPIO up, depended of the pin number and input and ouput option.
        pin : is the number of the pin taken from the boardlayout.
        io : string : is the pin should act as an input or output, [INPUT,OUTPUT]
        pull_up_down : string : Deciding to use either pull-up or pull-down. This option is only possible when a pin is an input channel.
        """
        if io == 'INPUT' and pull_up_down == 'Pull_UP':
            GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        elif io == 'INPUT' and pull_up_down == 'Pull_DOWN':
            GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        elif io == 'OUTPUT' and pull_up_down == 'Pull_UP':
            GPIO.setup(pin,GPIO.OUT,pull_up_down=GPIO.PUD_UP)
        elif io == 'OUTPUT' and pull_up_down == 'Pull_DOWN':
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
