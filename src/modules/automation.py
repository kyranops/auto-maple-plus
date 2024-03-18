import pyautogui
import mss
import cv2
import src.common.config as config, src.common.utils as utils
import src.gui.automation as automation
from src.gui.automation.main import AutomationParams
import pyotp
import time
import random

# The Elite Boss's warning sign
REVIVE_TEMPLATE = cv2.imread('assets/revive.png', 0)
MAPLE_ID_FIELD = cv2.imread('assets/mapleIDField.png', 0)
PASSWORD_FIELD = cv2.imread('assets/passwordField.png', 0)
WORLD = cv2.imread('assets/aquila.png', 0)

def autoRevive():
    frame = config.capture.frame #entire screen
    okButtonPos = utils.multi_match(frame, REVIVE_TEMPLATE, 0.8)[0]
    pyautogui.click(x=okButtonPos[0]+config.capture.window["left"],y=okButtonPos[1]+config.capture.window["top"])
    pyautogui.move(0,50)

def autoLogin():
    time.sleep(0.5) #slow it down abit because it is 2fast2scary
    try:
        frame = config.capture.frame #entire screen
        username = AutomationParams('Automation Settings').get("auto_login_username")
        password = AutomationParams('Automation Settings').get("auto_login_pw1")
        secretKey = AutomationParams('Automation Settings').get("auto_2FA_secretkey")
        world = (AutomationParams('Automation Settings').get("auto_world")).lower()

        w2press = {
            "aquila":4,
            "bootes":3,
            "cassiopeia":2,
            "delphinus":1
        }
        
        #input username
        usernamePos = utils.multi_match(frame, MAPLE_ID_FIELD, threshold=0.8)
        if usernamePos != []:
            pyautogui.click(x=int(usernamePos[0][0])+int(config.capture.window["left"]),y=int(usernamePos[0][1])+int(config.capture.window["top"]))
            pyautogui.write(username)
        
        #input password
        passwordPos = utils.multi_match(frame, PASSWORD_FIELD, threshold=0.8)
        if passwordPos != []:
            pyautogui.click(x=int(passwordPos[0][0])+int(config.capture.window["left"]),y=int(passwordPos[0][1])+int(config.capture.window["top"]))
            pyautogui.write(password)
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(0.5)

            #input OTP
            totp = pyotp.TOTP(secretKey)
            pyautogui.write(totp.now())
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(2)

            #choose world
            numPress = w2press[world]
            pyautogui.press("down",presses=numPress)
            time.sleep(0.5)
            pyautogui.press("enter")
            #choose channel
            desiredChannel = random.randint(1,30)
            downMoves = int(round(desiredChannel/5,0))
            rightMoves = int(desiredChannel%5)
            pyautogui.press("down",presses=downMoves)
            pyautogui.press("right",presses=rightMoves)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.press("enter")
    except Exception as e:
        print(e)

def auto2ndPW():
    frame = config.capture.frame #entire screen
    secondPassword = AutomationParams('Automation Settings').get("auto_2ndPW_pw2")
    clickOffset = 5
    xoffset = config.capture.window["left"]
    yoffset = config.capture.window["top"]

    shiftPos = cv2.imread("assets/onscreenKB/shift.png",0)

    for char in secondPassword:
        if char.isupper():
            charofInterest = cv2.imread("assets/onscreenKB/"+"{}.png".format(char.lower()),0)
            #find location
            charPos = utils.multi_match(frame,charofInterest,threshold=0.9)
            #shift
            shiftPos = utils.multi_match(frame,shiftPos, threshold=0.9)
            pyautogui.click(x=shiftPos[0][0]+xoffset,y=shiftPos[0][1]+yoffset)
            #click key
            pyautogui.click(x=(charPos[0][0]+clickOffset+xoffset),y=(charPos[0][1]+clickOffset+yoffset))
            #unshift
            pyautogui.click(x=shiftPos[0][0]+xoffset,y=shiftPos[0][1]+yoffset)
        else: 
            #input
            charofInterest = cv2.imread("assets/onscreenKB/"+"{}.png".format(char),0)
            charPos = utils.multi_match(frame,charofInterest, threshold=0.9)
            pyautogui.click(x=(charPos[0][0]+clickOffset+xoffset),y=(charPos[0][1]+clickOffset+yoffset))

    pyautogui.press("enter")