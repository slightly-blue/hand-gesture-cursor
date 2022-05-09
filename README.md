# hand-gesture-cursor
 Experimentation with different methods to convert hand gestures to mouse events. Not limited to any specific programing language or packages.

- Google MediaPipe as base


## Three Directions

1. **npm module** 
  - will only work in the confined space of a webapp  
  - might be very slow
  - can be deployed to a website in order to collect feedback
  - easily change cursor display for more info

2. **Python program** 
  - will work in any program
  - real world use can be tested

3. **C++ program**
  - will work in any program
  - better performance than python
  - more developer time, less libraries, less knowledge 

## Plan

- `Python`: *(PoC and testing)*
- `C++`: *(End product, probably out of scope for my research)*

## PoC Scope

- mediapipe library working, track hands, check distance between points

- fire a touch or click event in windows, linux or mac  


## TODO
- test if hybrid input injection is possible 
- test that staged inputs like click-drag-release for scrolling is possible  




Det finns redan implementeringar för att utföra mus klick events på basis av image recognition 
men problemet med dessa är att de inte är exacta och endast stöder mus klickningar.   

En mycket mera logisk lösning vore att emulera touch events eftersom det ger en tillgång till 
flera rörelser som är mera intuitiva. 
Det skulle automatiskt ge en möjlighet att scrolla, zooma, swipe och rotera.  

ett annat alternativ är att emulera en gamepad eller HOTAS controller, det skulle ge en friheten att leka med z axeln 
en ide är att bygga det som en unity modul, det skulle ge en möjlighet att röra på object i 3d space 




1. En executable (skapad med pyinstaller) som temporärt låter din webcam fungera som ett touch input device 
- Ett system för att konvertera mediapipe hand data till touch inputs 
- Ett python bibliotek för att emulera touch input i windows.


Converting and cleaning ML Mediapipe Hands data to windows touch input

Processing ML Mediapipe Hands data to emulate a touch input device on windows 


LeapMotion is better in security, quality and comfort. Only advantage is price since it doesn't require specialized hardware. 

Possible use cases:
- cheap developer testing of touch input in windows
- input control for games 






## **Gestures**

**V1**
mouse position 
left click 
right click
drag and drop


**V2**
tap
press and hold
slide
swipe
turn
pinch
stretch

## Ideas 

1. Touch emulation
2. Gamepad/H.O.T.A.S. emulation 
3. Mouse emulation 


Emulation Ideas:
- Virtual COM Ports 
- opensource library or api to emulate touch events 

- xbox python emulator exist

Emulation Problems:
- needs to be touch 
- needs to show cursor 

Strategy:
1. Emulate USB device, drivers already exist 



**Gesture emulation strategy**
move:             -  emulate pen or mouse 
tap:              -  emulate pen or mouse 
press and hold:   -  emulate pen or mouse 
drag:             -  emulate pen or mouse 
turn:             -  emulate touch 
pinch/stretch:    -  emulate touch
cross-slide       -  emulate touch 

What are the benefits of emulating a pen? 
- scrolling and swiping is possible with one hand 


for single hand events emulate a mouse



## What is the end product? 
En executable (skapad med pyinstaller) som temporärt gör din webcam till ett touch input device 


Leap Motion 
Siemens 


## References
[google mediapipe hands (paper)](https://arxiv.org/abs/2006.10214)
[Simulating Touch Input in Windows Using Touch Injection API](https://social.technet.microsoft.com/wiki/contents/articles/6460.simulating-touch-input-in-windows-8-using-touch-injection-api.aspx?PageIndex=2)
[A SYSTEMATIC COLLECTION OF NATURAL INTERACTIONS FOR IMMERSIVE MODELING FROM BUILDING BLOCKS](https://www.cambridge.org/core/journals/proceedings-of-the-design-society/article/systematic-collection-of-natural-interactions-for-immersive-modeling-from-building-blocks/59755C727679258E3B3A926DD52B040E)
[Gesture controlled CAD](https://dmf-lab.co.uk/gesture-controlled-cad/)
[SpaceX Gesture control experiment](https://www.youtube.com/watch?v=xNqs_S-zEBY)
[Leap Motion](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Leap+Motion+Controller&btnG=)




**Emulation research**
[touch-base proprietary API](https://support.touch-base.com/Documentation/50117/Application-Programming-Interface)
[windows hardware driver documentation](https://docs.microsoft.com/en-us/windows-hardware/drivers/)
[windows virtual hid framework](https://docs.microsoft.com/en-gb/windows-hardware/drivers/hid/virtual-hid-framework--vhf-)
[FreePIE: converting gamepad input](https://andersmalmgren.github.io/FreePIE/)
[FakeInput: ](https://github.com/uiii/FakeInput)
[InputEmulator: keyboard and mouse only](https://github.com/behzad62/InputEmulator)
[cs file](https://stackoverflow.com/questions/3352529/wpf-is-there-a-possibility-to-route-ordinary-mouse-events-to-touch-events-in/4652169#4652169)
[USB-HID emulation project](https://www.codeproject.com/Articles/1001891/A-USB-HID-Keyboard-Mouse-Touchscreen-emulator-with)