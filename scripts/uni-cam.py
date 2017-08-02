#!/usr/bin/env python

import colorsys
import signal
import time
from sys import exit
import sys
import os
from twython import Twython
import picamera
from gpiozero import Button

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

import unicornhathd

unicornhathd.rotation(45)


# SETUP
# Twitter API Keys
consumer_key = 'NObwoqPLvyLxGEiKZtNmwPeDn'
consumer_secret = 'u7vDB7szLODhX30Y2wn94vPdo1W775xKudSL7LrUctcyL2md87'
access_token = '886150536550129664-jdrKTgRrCizUnmEGFIuV9Dm0U4TLYuI'
access_token_secret = 'ZnbQt7hnGVgLicBKgQWUZFE8AlkuVi5AFPUqB9R87IWIf'

button_pin = 2

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

#TEXT = "GET READY!!! .... 3 .... 2 .... 1 .... SAY CHEESE!!!"
TEXT = "SMILE!!!"
FONT = ("/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf", 20)


def take_photo():

    white_flash(.1,.1)
    white_flash(.1,.1)
    white_flash(.1,.1)
    white_flash(.1,.1)

    print("starting to take photo")

    # turn on all the pixels
    for x in xrange(0, 16):
        for y in xrange(0, 16):
                unicornhathd.set_pixel(x, y, 255, 255, 255)

    unicornhathd.show()

    timestamp = str(time.time())
    image_path = "/home/pi/uni-cam/web/pics/" + timestamp + ".jpg"
    thumb_path = image_path.replace("/pics/", "/thumbs/")
    camera = picamera.PiCamera()
    camera.resolution = (2048, 1456)
    camera.capture(image_path)

    print("photo acquired")

    unicornhathd.off()

    print("starting tweet")
    photo = open(image_path, 'rb')
    image = twitter.upload_media(media=photo)
    message = "Tweeted with Unicam at Amsterjam!"
    twitter.update_status(status=message, media_ids=[image['media_id']])
    print("tweet complete")

    print("generating thumbnail")
    im = Image.open(image_path)
    im.thumbnail((400, 400), Image.ANTIALIAS)
    im.save(thumb_path, "JPEG")
    print("thumbnail done")


def draw_text(FONT, TEXT):

    print("drawing text")

    unicornhathd.brightness(0.6)

    text_x = 0
    text_y = -6

    width, height = unicornhathd.get_shape()

    font_file, font_size = FONT

    font = ImageFont.truetype(font_file, font_size)

    text_width, text_height = font.getsize(TEXT)

    text_width += width + text_x

    image = Image.new("RGB", (text_width,max(16, text_height)), (0,0,0))
    draw = ImageDraw.Draw(image)

    draw.text((text_x, text_y), TEXT, fill=(255, 255, 255), font=font)

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x+scroll, y))

                br, bg, bb = [int(n * 255) for n in colorsys.hsv_to_rgb((x + scroll) / float(text_width), 1.0, 1.0)]
                r, g, b = [float(n / 255.0) for n in pixel]
                r = int(br * r)
                g = int(bg * g)
                b = int(bb * b)

                unicornhathd.set_pixel(width-1-x, y, r, g, b)

        unicornhathd.show()
        time.sleep(0.01)


    print("drawing text done")

def white_flash(on,off):

    print("flash on")

    for x in xrange(0, 16):
        for y in xrange(0, 16):
                unicornhathd.set_pixel(x, y, 255, 255, 255)

    unicornhathd.brightness(1)
    unicornhathd.show()
    time.sleep(on)
    unicornhathd.off()
    time.sleep(off)

    print("drawing off")


def uni_cam():

    draw_text(FONT, TEXT)

    take_photo()


#button = Button(button_pin)
#button.when_pressed = uni_cam

uni_cam()

unicornhathd.off()
