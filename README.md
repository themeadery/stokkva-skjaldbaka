# støkkva skjaldbaka

støkkva skjaldbaka translates to "Snapping Turtle" in Old Norse, or at least Icelandic (which is apparently similar)

"Snap" because the program triggers the camera to snap photos  
"Turtle" because timelapses are slow and take a lot of time

## Idea/Workflow

Capture an image and transfer -> Measure brightness -> Adjust settings -> Capture another image -> repeat

## Why?

- The X-T1 bult-in intervalometer is limited to 999 shots
- You don't want to buy a bigger memory card
- You don't want to buy an expensive intervalometer
- There is no info on the interface when shooting timelapses, so you can't see your exposure meter or histogram and adjust accurately
- Conditions are changing during the shoot
- You want to ramp day-to-night/holy grail

## Requires

- Python 3.x
- gphoto2
- exiftool
- ImageMagick (v7.x recommended)
- USB cable
- Change the USB mode to "PC SHOOT AUTO" or "PC SHOOT FIXED" (Recommended)

## Commands

    $ python stokkva.py
    støkkva skjaldbaka started

## Problems

#### gphoto errors when issuing commands:

    $ ps aux | grep gphoto
    $ kill -9 {pid of gvfs-gphoto2-volume-monitor}
or

    $ sudo chmod -x /usr/lib/gvfs/gvfs-gphoto2-volume-monitor
    $ sudo chmod -x /usr/lib/gvfs/gvfsd-gphoto2
You probably need to power cycle the camera after fixing these problems

The "PC SHOOT FIXED" USB option in the X-T1 says it will not save to the memory card, but it still does. Take out the memory card if you don't want it to fill up or be the limitation of your duration. Might also speed up the process, since it isn't trying to write data twice.

Your shutter dial needs to be in the "T" position to accept shutter speed change commands.

My X-T1 shuts off pretty quick if it is tethered and no commands are sent. Seems like about 1 minute timeout. Must power cycle the camera to reconnect.

Sometimes the camera refuses to shut off while still plugged in to USB.

## Credit

Based on <https://github.com/dps/rpi-timelapse>  
I did not fork his project because it is more complicated than I needed and it is based on python2.

## TODO

- ISO ramping - Doesn't respond to the --set-config command
