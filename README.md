
Welcome to my dragonfly scripts repository.

## Vim
The most notable file here is the one for Vim.
The Pycharm and Visual Studio grammars branch off it,
and they assume you have a Vim plug-in installed.
Commands may be spoken one after another without stopping, 
so long as there is at most one command in the sequence that changes modes (normal, visual, insert, ex).
The Chrome grammar also assumes you are using the Vimium plug-in.

## Changing files
Note that if you change one of the files,
you will need to turn your mic off and back on again.
Dragon calls each module's unload function when you turn the mic back on again,
_not_ when you turn it off.
Then it reruns your module in the same Python environment.
If you made a change in any imported modules from your module, 
then you will need to restart all of Dragon, not just turn the mic off,
because Python will not import the same module multiple times.

## Hardware and Software
Hardware quality is essential. 
The difference in usability is night and day with proper hardware 
(comparing mostly to the builtin hardware in my laptop).

I use:
- Dragon NaturallySpeaking 15 professional individual, 
    - **Windows Speech Recognition (WSR) cannot substitute**
    - Commands only mode, not Dication+Commands 
- Dictation-toolbox/dragonfly
- Natlink 4.2
- Python 2.7 (will be upgrading as soon as a Natlink release supporting Python 3 is released)
- SpeechWare FlexyMike Dual Ear Cardioid microphone
    - plugged in through the SpeechWare USB MultiAdapter it comes with, in normal mode
- Tobii Eye Tracker 5
    - PrecisionGazeMouse for eye-tracking mouse control
- Logitech C922 Pro HD Stream Webcam
    - Eviacam for head-tracking to enhance precision of mouse control
    - (Optional) UBeesize Mini Led Camera Ringlight in warm mode for consitent face lighting
- Windows 10 (I've read 7 works better, but I cannot confirm.)
- HP Spectre touch screen laptop if ever I must click natively
- Kinesis Advantage2 Linear Feel keyboard if ever I must type
