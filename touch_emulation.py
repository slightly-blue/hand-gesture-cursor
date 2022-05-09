# Credit:
# https://stackoverflow.com/questions/15878478/emulate-touch-event-in-windows-8-using-python

from ctypes import *
from ctypes.wintypes import *

#Constants
# Docs https://docs.microsoft.com/en-us/windows/win32/inputmsg/constants
#For touchMask
TOUCH_MASK_NONE=          0x00000000 #Default
TOUCH_MASK_CONTACTAREA=   0x00000001
TOUCH_MASK_ORIENTATION=   0x00000002
TOUCH_MASK_PRESSURE=      0x00000004
TOUCH_MASK_ALL=           0x00000007

#For touchFlag
TOUCH_FLAG_NONE=          0x00000000


#For PenMask
PEN_MASK_NONE =           0x00000000
PEN_MASK_PRESSURE =       0x00000001
PEN_MASK_ROTATION =       0x00000002
PEN_MASK_TILT_X =         0x00000004
PEN_MASK_TILT_Y =         0x00000008

#For PenFlags
PEN_FLAG_NONE=            0x00000000
PEN_FLAG_BARREL=          0x00000001
PEN_FLAG_INVERTED=        0x00000002
PEN_FLAG_ERASER=          0x00000004




#For pointerType
PT_POINTER=               0x00000001#All
PT_TOUCH=                 0x00000002
PT_PEN=                   0x00000003
PT_MOUSE=                 0x00000004

#For pointerFlags
POINTER_FLAG_NONE=        0x00000000#Default
POINTER_FLAG_NEW=         0x00000001
POINTER_FLAG_INRANGE=     0x00000002
POINTER_FLAG_INCONTACT=   0x00000004
POINTER_FLAG_FIRSTBUTTON= 0x00000010
POINTER_FLAG_SECONDBUTTON=0x00000020
POINTER_FLAG_THIRDBUTTON= 0x00000040
POINTER_FLAG_FOURTHBUTTON=0x00000080
POINTER_FLAG_FIFTHBUTTON= 0x00000100
POINTER_FLAG_PRIMARY=     0x00002000
POINTER_FLAG_CONFIDENCE=  0x00004000
POINTER_FLAG_CANCELED=    0x00008000
POINTER_FLAG_DOWN=        0x00010000
POINTER_FLAG_UPDATE=      0x00020000
POINTER_FLAG_UP=          0x00040000
POINTER_FLAG_WHEEL=       0x00080000
POINTER_FLAG_HWHEEL=      0x00100000
POINTER_FLAG_CAPTURECHANGED=0x00200000



POINTER_FEEDBACK_INDIRECT = 2

#Structs Needed

class POINTER_INFO(Structure):
    _fields_=[("pointerType",c_uint32),
              ("pointerId",c_uint32),
              ("frameId",c_uint32),
              ("pointerFlags",c_int),
              ("sourceDevice",HANDLE),
              ("hwndTarget",HWND),
              ("ptPixelLocation",POINT),
              ("ptHimetricLocation",POINT),
              ("ptPixelLocationRaw",POINT),
              ("ptHimetricLocationRaw",POINT),
              ("dwTime",DWORD),
              ("historyCount",c_uint32),
              ("inputData",c_int32),
              ("dwKeyStates",DWORD),
              ("PerformanceCount",c_uint64),
              ("ButtonChangeType",c_int)
              ]


class POINTER_TOUCH_INFO(Structure):
    _fields_=[("pointerInfo",POINTER_INFO),
              ("touchFlags",c_int),
              ("touchMask",c_int),
              ("rcContact", RECT),
              ("rcContactRaw",RECT),
              ("orientation", c_uint32),
              ("pressure", c_uint32)]

class POINTER_PEN_INFO(Structure):
        _fields_=[("pointerInfo",POINTER_INFO),
              ("penFlags",c_int),
              ("penMask",c_int),
              ("pressure",c_uint32),
              ("rotation", c_uint32),
              ("tiltX", c_int32),
              ("tiltY", c_int32)]


class SYNTHETICPOINTERDEVICE(Structure):
    _fields_=[
        ("pointerType", c_int),
        ("maxCount", c_int),
        ("mode", c_int),
    ]
# HSYNTHETICPOINTERDEVICE CreateSyntheticPointerDevice(
#   [in] POINTER_INPUT_TYPE    pointerType,
#   [in] ULONG                 maxCount,
#   [in] POINTER_FEEDBACK_MODE mode
# );

#Initialize Pointer and Touch info

pointerInfo=POINTER_INFO(pointerType=PT_TOUCH,
                         pointerId=0,
                         ptPixelLocation=POINT(950,540),
                         sourceDevice=0,
                         )

touchInfo=POINTER_TOUCH_INFO(pointerInfo=pointerInfo,
                             touchFlags=TOUCH_FLAG_NONE,
                             touchMask=TOUCH_MASK_ALL,
                             rcContact=RECT(pointerInfo.ptPixelLocation.x-5,
                                  pointerInfo.ptPixelLocation.y-5,
                                  pointerInfo.ptPixelLocation.x+5,
                                  pointerInfo.ptPixelLocation.y+5),
                             orientation=90,
                             pressure=32000)

# Docs: https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-pointer_pen_info
pointerPenInfo=POINTER_PEN_INFO(pointerInfo=pointerInfo,
                             penFlags=POINTER_FLAG_NONE,
                             penMask=PEN_MASK_PRESSURE | PEN_MASK_ROTATION | PEN_MASK_TILT_X | PEN_MASK_TILT_Y,
                            #  rcContact=RECT(pointerInfo.ptPixelLocation.x-5,
                            #       pointerInfo.ptPixelLocation.y-5,
                            #       pointerInfo.ptPixelLocation.x+5,
                            #       pointerInfo.ptPixelLocation.y+5),
                             #orientation=90,
                             pressure=1024, # A pen pressure normalized to a range between 0 and 1024.
                             rotation=0,  # The clockwise rotation, or twist, of the pointer normalized in a range of 0 to 359.
                             tiltX=0, # The angle of tilt of the pointer along the x-axis in a range of -90 to +90
                             tiltY=0,
                             )


def make_touch(x,y,fingerRadius):
    touchInfo.pointerInfo.ptPixelLocation.x=x
    touchInfo.pointerInfo.ptPixelLocation.y=y

    touchInfo.rcContact.left=x-fingerRadius
    touchInfo.rcContact.right=x+fingerRadius
    touchInfo.rcContact.top=y-fingerRadius
    touchInfo.rcContact.bottom=y+fingerRadius

    #Initialize Touch Injection
    if (windll.user32.InitializeTouchInjection(1,1) != 0):
        print("Initialized Touch Injection")


    #Press Down
    touchInfo.pointerInfo.pointerFlags=(POINTER_FLAG_DOWN|POINTER_FLAG_INRANGE|POINTER_FLAG_INCONTACT)

    if (windll.user32.InjectTouchInput(1, byref(touchInfo))==0):
        print("Failed with Error: "+ FormatError())
    else:
        print("Touch Down Succeeded!")


    #Pull Up
    touchInfo.pointerInfo.pointerFlags=POINTER_FLAG_UP

    if (windll.user32.InjectTouchInput(1,byref(touchInfo))==0):
        print("Failed with Error: "+FormatError())
    else:
        print("Pull Up Succeeded!")


    windll.user32.ShowCursor(c_bool(1))
    return


def initiate_touch(x,y):
    touchInfo.pointerInfo.ptPixelLocation.x=x
    touchInfo.pointerInfo.ptPixelLocation.y=y
    touchInfo.pointerInfo.pointerId=0

    touchInfo.rcContact.left=x-2
    touchInfo.rcContact.right=x+2
    touchInfo.rcContact.top=y-2
    touchInfo.rcContact.bottom=y+2

    #Initialize Touch Injection
    if (windll.user32.InitializeTouchInjection(1,1) != 0):
        print("Initialized Touch Injection")


    #Press Down
    touchInfo.pointerInfo.pointerFlags=(POINTER_FLAG_DOWN|POINTER_FLAG_INRANGE|POINTER_FLAG_INCONTACT)

    if (windll.user32.InjectTouchInput(1, byref(touchInfo))==0):
        print("Failed with Error: "+ FormatError())
    else:
        print("Touch Down Succeeded!")

    return

def release_touch(x,y):
    touchInfo.pointerInfo.ptPixelLocation.x=x
    touchInfo.pointerInfo.ptPixelLocation.y=y
    touchInfo.pointerInfo.pointerId=0
    touchInfo.rcContact.left=x-2
    touchInfo.rcContact.right=x+2
    touchInfo.rcContact.top=y-2
    touchInfo.rcContact.bottom=y+2

    
    #Initialize Touch Injection
    if (windll.user32.InitializeTouchInjection(1,1) != 0):
        print("Initialized Touch Injection")

    #Pull Up
    touchInfo.pointerInfo.pointerFlags=POINTER_FLAG_UP

    if (windll.user32.InjectTouchInput(1,byref(touchInfo))==0):
        print("Failed with Error: "+FormatError())
    else:
        print("Pull Up Succeeded!")

    return

def drag_touch(x,y):
    touchInfo.pointerInfo.ptPixelLocation.x=x
    touchInfo.pointerInfo.ptPixelLocation.y=y
    touchInfo.pointerInfo.pointerId=0
    touchInfo.rcContact.left=x-2
    touchInfo.rcContact.right=x+2
    touchInfo.rcContact.top=y-2
    touchInfo.rcContact.bottom=y+2

    
    #Initialize Touch Injection
    if (windll.user32.InitializeTouchInjection(1,1) != 0):
        print("Initialized Touch Injection")

    # Update drag
    touchInfo.pointerInfo.pointerFlags = POINTER_FLAG_UPDATE | POINTER_FLAG_INRANGE | POINTER_FLAG_INCONTACT

    if (windll.user32.InjectTouchInput(1,byref(touchInfo))==0):
        print("Failed with Error: "+FormatError())
    else:
        print("Pull Up Succeeded!")

    return



def drag_emulation(x1,y1):
    touchInfo.pointerInfo.ptPixelLocation.x=x1
    touchInfo.pointerInfo.ptPixelLocation.y=y1
    touchInfo.pointerInfo.pointerId=0
    touchInfo.rcContact.left=x1-2
    touchInfo.rcContact.right=x1+2
    touchInfo.rcContact.top=y1-2
    touchInfo.rcContact.bottom=y1+2

    #Initialize Touch Injection
    if (windll.user32.InitializeTouchInjection(1,1) != 0):
        print("Initialized Touch Injection")

    #Press Down
    touchInfo.pointerInfo.pointerFlags=(POINTER_FLAG_DOWN|POINTER_FLAG_INRANGE|POINTER_FLAG_INCONTACT)
    if (windll.user32.InjectTouchInput(1, byref(touchInfo))==0):
        print("Failed with Error: "+ FormatError())
    else: print("Touch Down Succeeded!")

    # Update drag
    touchInfo.pointerInfo.pointerFlags = POINTER_FLAG_UPDATE | POINTER_FLAG_INRANGE | POINTER_FLAG_INCONTACT

    for x in range(500):
        touchInfo.pointerInfo.ptPixelLocation.x = touchInfo.pointerInfo.ptPixelLocation.x - 1
        windll.user32.InjectTouchInput(1,byref(touchInfo))
 
    #Pull Up
    touchInfo.pointerInfo.pointerFlags=POINTER_FLAG_UP

    if (windll.user32.InjectTouchInput(1,byref(touchInfo))==0):
        print("Failed with Error: "+FormatError())
    else: print("Pull Up Succeeded!")

    return


#Ex:
#makeTouch(950,270,5)


# Pointer is probably the wrong way since we can only provide one input 
# Figure out another way to display cursor 

def pointer_click(x,y):
    # CreateSyntheticPointerDevice.
    # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-injectsyntheticpointerinput
    # https://docs.microsoft.com/en-us/windows/win32/inputmsg/messages-and-notifications-portal

    pointerPenInfo.pointerInfo.ptPixelLocation.x=x
    pointerPenInfo.pointerInfo.ptPixelLocation.y=y
    pointerPenInfo.pointerInfo.ptPixelLocation.y=y
    pointerPenInfo.pointerInfo.ptPixelLocation.y=y
    pointerPenInfo.pressure  = 1024
    pointerPenInfo.tiltX  = 0
    pointerPenInfo.tiltY  = 0

    pointerPenInfo.penMask = PEN_MASK_PRESSURE
    pointerPenInfo.penFlags = PEN_FLAG_NONE

    # These apparently need to be 0
    # curtesy of:  https://github.com/gsbischoff/usb-pen-injection/blob/master/PenClient.c
    pointerPenInfo.pointerInfo.dwTime = 0
    pointerPenInfo.pointerInfo.PerformanceCount = 0

    # Initialize Synthetic Pointer Device
    
    pointerDeviceHandle = windll.user32.CreateSyntheticPointerDevice(PT_PEN,1,POINTER_FEEDBACK_INDIRECT) #, POINTER(c_ulong)

    if (pointerDeviceHandle != 0):
        print("Initialized Synthetic Pointer Device. Handle id: " + str(pointerDeviceHandle))
    else: print("Synthetic Pointer Device Initialization failed with error: " + FormatError())

    pointerPenInfo.pointerInfo.sourceDevice = pointerDeviceHandle
    # Press Down
    pointerPenInfo.pointerInfo.pointerFlags=(POINTER_FLAG_DOWN | POINTER_FLAG_INRANGE | POINTER_FLAG_INCONTACT | POINTER_FLAG_PRIMARY)

    # ctypes.ArgumentError: argument 1: <class 'TypeError'>: Don't know how to convert parameter 1
    if ( not windll.user32.InjectSyntheticPointerInput(pointerDeviceHandle, byref(pointerPenInfo), 0x00000001)):
        print("Failed with Error: "+ FormatError())
    else:
        print("Touch Down Succeeded!")

    print("Post touch down Log: " + FormatError())

    # Pull Up
    pointerPenInfo.pointerInfo.pointerFlags=POINTER_FLAG_UP

    if (not windll.user32.InjectSyntheticPointerInput(pointerDeviceHandle, byref(pointerPenInfo), 0x00000001)):
        print("Failed with Error: "+FormatError())

    else:
        print("Pull Up Succeeded!")

    windll.user32.DestroySyntheticPointerDevice(pointerDeviceHandle)
    print("Last Log: " + FormatError())

    print(WinError(get_last_error()))

    # I could be missing some flag or value unique to pen events 
    # 



    return




#MOUSEEVENT_MOVE = 1 # it's better to keep that as variable

MOUSEEVENTF_MOVE = 0x0001 # mouse move 
MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down 
MOUSEEVENTF_LEFTUP = 0x0004 # left button up 
MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down 
MOUSEEVENTF_RIGHTUP = 0x0010 # right button up 
MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down 
MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up 
MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled 
MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move 

PUL = POINTER(c_ulong)

class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]

class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", Input_I)]

def move_cursor(x,y):
    """https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput"""

    #current_x, current_y = win32api.GetCursorPos()
    #windll.user32.mouse_event(MOUSEEVENTF_MOVE, x - current_x, y - current_y, 0, 0)
    #windll.user32.mouse_event(MOUSEEVENT_ABSOLUTE, x, y, 0, 0)
    #windll.user32.ShowCursor(c_bool(1))
    #windll.user32.SetCursorPos(x,y)

    x = 1 + int(x * 65536./1920.)
    y = 1 + int(y * 65536./1080.)
    extra = c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE), 0, pointer(extra))
    command = Input(c_ulong(0), ii_)
    windll.user32.SendInput(1, pointer(command), sizeof(command))
        
    return True
