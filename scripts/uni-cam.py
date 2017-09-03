#!/usr/bin/env python

import colorsys
from signal import pause
import time
from sys import exit
import sys
import os
from twython import Twython
import picamera
from gpiozero import Button

# define camera
camera = picamera.PiCamera()

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
twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

FONT = ("/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf", 20)

button_pin = 21

def take_photo():

    draw_text(FONT, "GET READY!!! .... 3 .... 2 .... 1 .... SAY CHEESE!!!")

    white_flash(.1,.1)
    white_flash(.1,.1)
    white_flash(.1,.1)
    white_flash(.1,.1)
    bright_white()

    timestamp = str(time.time())
    image_path = "/home/pi/uni-cam/web/pics/" + timestamp + ".jpg"

    camera.resolution = (1024, 728)
    camera.capture(image_path)

    unicornhathd.off()

    draw_text(FONT, "PHOTO TAKEN - SENDING TO TWITTER!")

    make_thumb(image_path)
    send_tweet(image_path)

    draw_text(FONT, "DONE! FOLLOW @AMSTERJAM__ TO SEE YOUR PHOTO!")


def make_thumb(image_path):
    thumb_path = image_path.replace("/pics/", "/thumbs/")
    im = Image.open(image_path)
    im.thumbnail((400, 400), Image.ANTIALIAS)
    im.save(thumb_path, "JPEG")

def send_tweet(image_path):
    photo = open(image_path, 'rb')
    image = twitter.upload_media(media=photo)
    message = "Tweeted with Unicam at Amsterjam!"
    twitter.update_status(status=message, media_ids=[image['media_id']])

# fancy pants function to draw scrolling rainbow text
def draw_text(FONT, TEXT):

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


def bright_white():
    # turn on all the pixels
    for x in xrange(0, 16):
        for y in xrange(0, 16):
            unicornhathd.set_pixel(x, y, 255, 255, 255)

    unicornhathd.show()

def white_flash(on,off):

    for x in xrange(0, 16):
        for y in xrange(0, 16):
                unicornhathd.set_pixel(x, y, 255, 255, 255)

    unicornhathd.brightness(1)
    unicornhathd.show()
    time.sleep(on)
    unicornhathd.off()
    time.sleep(off)


button = Button(21)
button.when_pressed = take_photo
pause()
