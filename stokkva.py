from datetime import datetime
from datetime import timedelta
import time
from itertools import count
import subprocess
import os

MIN_BRIGHTNESS = 18000
MAX_BRIGHTNESS = 25000

def reset():
    print("Resetting connection to camera...")
    subprocess.run(["gphoto2", "--reset"])
    print("Connection reset")

def get_shutter_speed():
    print("Getting Shutter Speeds...")
    out = subprocess.check_output(["gphoto2", "--get-config", "shutterspeed"])
    out = out.decode()
    #print(out) #Debug
    shutter_choices = {}
    for line in out.split('\n'):
        if line.startswith('Choice:'):
            shutter_choices[line.split(' ')[2]] = line.split(' ')[1]
        if line.startswith('Current:'):
            shutter_current_choice = line.split(' ')[1]
    return shutter_current_choice, shutter_choices

def get_iso():
    print("Getting ISO Speeds...")
    out = subprocess.check_output(["gphoto2", "--get-config", "iso"])
    out = out.decode()
    #print(out) #Debug
    iso_choices = {}
    for line in out.split('\n'):
        if line.startswith('Choice:'):
            iso_choices[line.split(' ')[2]] = line.split(' ')[1]
        if line.startswith('Current:'):
            iso_current_choice = line.split(' ')[1]
    return iso_current_choice, iso_choices

def capture_image_and_download(filename):
    print("\nCapturing Image...")
    out = subprocess.check_output(["gphoto2", "--capture-image-and-download", "--force-overwrite", "--filename", filename])
    print("Downloading...")
    out = out.decode()
    for line in out.split("\n"):
        if line.startswith("Saving file as "):
            filename = line.split("Saving file as ")[1]
    print(f"Downloaded image {filename}")
    return filename

def measure_brightness(filename):
    print(f"Measuring brightness of {filename}...")
    print(f"Extracting preview of {filename}...")
    subprocess.run(["exiftool", "-b", "-PreviewImage", "-w", "_preview.jpg", filename])
    print("Extracted")
    preview = filename.strip(".RAF") + "_preview.jpg"
    out = subprocess.check_output(["identify", "-format", "%[mean]", preview])
    brightness = float(out.decode())
    print(f"Brightness is {brightness}")
    return brightness

def set_shutter_speed(shutter_choice):
    print(f"Setting shutterspeed to {shutter_choice}...")
    subprocess.run(["gphoto2", "--set-config", f"shutterspeed={shutter_choice}"]) # Note: will take a choice index or literal
    print("Shutter speed set")

def set_iso(iso_choice):
    print(f"Setting ISO to {iso_choice}...")
    subprocess.run(["gphoto2", "--set-config", f"iso={iso_choice}"])
    print("ISO set")

# Main
print("\nstøkkva skjaldbaka started\n")
reset() # Reset connection to camera just in case

# Get configs
shutter_current_choice, shutter_choices = get_shutter_speed()
# TODO: Don't do this below
# Read the shutter_current_choice from get_shutter_speed()
# Then match shutter_current_choice with dictionary from shutter_choices because it is a literal speed instead of a "choice"
# This will allow brightness if statement math below to increment by index of 1
shutter_choice = 22 # Set initial shutter speed to 1/30
set_shutter_speed(shutter_choice)
iso_current_choice, iso_choices = get_iso()

# Set timelapse parameters
interval = int(input("Enter Interval in seconds: ")) #Turn on when it's a real interactive program
#interval = 7 # Non interactive for pasting
interval = timedelta(seconds=interval)
length = int(input("Enter Total Number of Shots: ")) #Turn on when it's a real interactive program
#length = 20 # Non interactive for pasting

# Make capture directory
directory = "capture"
print("Creating capture directory...")
if os.path.isdir(directory):
    print("Capture directory already exists")
    # directory = directory + "1" # try to iterate a new directory
else:
    subprocess.run(["mkdir", directory])
    print("Directory created")

# Filename iterator
iterator = ("DSCF%04i.RAF" % i for i in count(1)) # Generate a new filename for each shot, starting with DSCF0001.raf

# Main loop
for x in range(length):
    started = datetime.now() # Start timing the operation
    filename = next(iterator) # Increment shot number by 1
    filename = capture_image_and_download(filename)
    brightness = measure_brightness(filename)
    if brightness < MIN_BRIGHTNESS and shutter_choice < len(shutter_choices) - 1: # TODO: check if exceeds interval, requires dictionary lookup
        shutter_choice = shutter_choice + 1
        set_shutter_speed(shutter_choice)
    elif brightness > MAX_BRIGHTNESS and shutter_choice > 0:
        shutter_choice = shutter_choice - 1
        set_shutter_speed(shutter_choice)
    ended = datetime.now() # Stop timing the operation
    if started and ended and ended - started < interval:
        print("Sleeping...")
        time.sleep((interval - (ended - started)).seconds)
