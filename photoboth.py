#!/usr/bin/env python
# -*- coding: utf-8 -*-

import picamera
import os
import time
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

overlay_renderer = None

def main():

    W = 1280
    H = 720
    BUTTON_GPIO = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pressed = False

    def text(text):
        global overlay_renderer
        img = Image.new("RGBA", (1280, 720), (255, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.font = ImageFont.truetype(
                        "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",
                        80)
        w, h = draw.textsize(text)
        draw.text(((W-w)/2,(H-h)/2), text, (255, 255, 255))

        if not overlay_renderer:
            overlay_renderer = camera.add_overlay(img.tobytes(),
                                                  layer=3,
                                                  size=img.size,
                                                  alpha=128);
        else:
            overlay_renderer.update(img.tobytes())

    with picamera.PiCamera() as camera:
        camera.resolution = (W), (H)
        camera.crop       = (0.0, 0.0, 1.0, 1.0)
        camera.start_preview()

        overlay_renderer = None

        while True:
            text(text = "Mache ein Foto mit dem Knopf")
            if not GPIO.input(BUTTON_GPIO):
                if not pressed:
                    text(text = "Auf die Plätze")
                    time.sleep(1.5)
                    text(text = "Fertig?")
                    time.sleep(1.5)
                    text(text = "Cheese!")
                    time.sleep(1)
                    date = ("data/" + (time.strftime("%Y%m%d-%H%M%S")) + ".png")
                    text(text = " ")
                    camera.capture((date), use_video_port=False)
                    time.sleep(3)


        else:
            pressed = False
        time.sleep(0.1)


if __name__ == '__main__':
    import sys
    main()