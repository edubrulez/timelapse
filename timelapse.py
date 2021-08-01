from picamera import PiCamera
from os import system
import datetime
from time import sleep

tlminutes = 1 #660 #set this to the number of minutes you wish to run your timelapse camera
secondsinterval = 5 #number of seconds delay between each photo taken
fps = 30 #frames per second timelapse video
numphotos = int((tlminutes*60)/secondsinterval) #number of photos to take
print("number of photos to take = ", numphotos)

dateraw= datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H%M")
print("RPi started taking photos for your timelapse at: " + datetimeformat)

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.vflip = True
camera.hflip = True

#system('rm /home/pi/Pictures/*.jpg') #delete all photos in the Pictures folder before timelapse start

for i in range(numphotos):
    camera.capture('/home/pi/Pictures/image{0:06d}.jpg'.format(i))
    sleep(secondsinterval)
print("Done taking photos.")
print("Please standby as your timelapse video is created.")

system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/Pictures/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/Videos/{}.mp4'.format(fps, datetimeformat))

usbdir= '/media/pi/8825-920F/{}/'.format(datetimeformat)
print("Moving photos to backup storage ".format(usbdir))
system('mkdir {}'.format(usbdir))
system('mv /home/pi/Pictures/*.jpg {}'.format(usbdir))

#system('rm /home/pi/Pictures/*.jpg')
print('Timelapse video is complete. Video saved as /home/pi/Videos/{}.mp4'.format(datetimeformat))
