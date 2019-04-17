import webbrowser

import cv2
import numpy as np
import pyautogui
import PIL
import time


def init():
	# TODO: Add more example websites with recaptcha
	webbrowser.open(
		'''https://jsso.indiatimes.com/sso/identity/register?channel=businessinsider&identifier=r@g.c'''
	)

	# Move to a temporary location and wait for window to open
	pyautogui.moveTo(1200, 200)
	time.sleep(5)


def get_coords():
	# Grab a screenshot and save it
	screenshot = PIL.ImageGrab.grab()
	screenshot.save("hay.png")

	# Convert the PIL image to an OpenCV one and read in the needle
	haystack = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
	needle = cv2.imread('needle.png')

	# Find the coordinates of the ReCaptcha logo
	diff = cv2.matchTemplate(haystack, needle, cv2.TM_CCORR_NORMED)
	x, y = np.unravel_index(np.argmax(diff), diff.shape)

	# Subtract offset of Checkbox from logo
	return x - 230, y + 60


def click_captcha(x, y):
	# Move to the captcha, but overshoot and then fine-tune
	pyautogui.moveTo(x - 28, y + 50, duration=0.5)
	pyautogui.moveTo(x + 3, y - 51, duration=0.20)
	pyautogui.moveTo(x, y, duration=0.2)

	# Pause momentarily before clicking
	time.sleep(0.2)
	pyautogui.click()

	# Once click has been registered, move away
	time.sleep(0.5)
	pyautogui.moveTo(x - 12, y + 42, duration=0.1)


def main():
	print("Starting...")
	init()

	print("Finding Captcha...")
	x, y = get_coords()
	print("Coords: (%d, %d)" % (x, y))

	click_captcha(x, y)
	print("Done!")


if __name__ == '__main__':
	main()
